from google import genai
from google.genai import types
import json
import PIL.Image
import os

# os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = './mydressr-project-ef3d96e53e7a.json'

client = genai.Client(
    vertexai=True, 
    project="mydressr-project",
    location="us-central1"
)

def analyze_clothing_image(file_obj) -> dict:
    if hasattr(file_obj, "read"):
        file_obj.seek(0)
        image_bytes = file_obj.read()
    else:
        with open(file_obj, "rb") as f:
            image_bytes = f.read()

    # Define a config to force JSON and lower safety barriers
    config = types.GenerateContentConfig(
        response_mime_type="application/json",
        safety_settings=[
            types.SafetySetting(
                category="HARM_CATEGORY_SEXUALLY_EXPLICIT",
                threshold="BLOCK_NONE", # High-waisted pants/shorts sometimes trigger this
            ),
            types.SafetySetting(
                category="HARM_CATEGORY_HATE_SPEECH",
                threshold="BLOCK_NONE",
            ),
        ]
    )

    response = client.models.generate_content(
        model="gemini-2.0-flash",
        config=config,
        contents=[
            types.Part.from_bytes(data=image_bytes, mime_type="image/jpeg"),
            "Analyze this clothing. Return JSON keys: category, color, occasion, weather_type."
        ]
    )

    # CHECK FOR NONE BEFORE PARSING
    if response.text is None:
        # Check if it was blocked
        finish_reason = "Unknown"
        if response.candidates and response.candidates[0].finish_reason:
            finish_reason = response.candidates[0].finish_reason
        
        return {
            "category": "Unknown",
            "color": "Unknown",
            "occasion": "Casual",
            "weather_type": "all weather",
            "error": f"AI blocked or empty response. Reason: {finish_reason}"
        }

    return json.loads(response.text)


def normalize_ai_result(ai_data: dict) -> dict:
    """
    Handles cases where AI returns lists instead of strings.
    """
    def first_value(value):
        if isinstance(value, list) and value:
            return value[0]
        return value

    return {
        "category": first_value(ai_data.get("category", "Uncategorized")),
        "color": first_value(ai_data.get("color", "Unknown")),
        "occasion": first_value(ai_data.get("occasion")),
        "weather_type": first_value(ai_data.get("weather_type", "all_weather")),
    }


def suggest_outfit(city, temp, humidity, condition, wardrobe_items):
    image_parts = []
    for item in wardrobe_items:
        if item.image:
            with item.image.open('rb') as f:
                image_bytes = f.read()
                image_parts.append(f"Item ID: {item.id}")
                image_parts.append(
                    types.Part.from_bytes(data=image_bytes, mime_type="image/jpeg")
                )

    prompt = f"""
        Role: Act as a professional Personal Stylist with expertise in color theory and seasonal dressing.
        
        Current Context:
        - City: {city}
        - Current Weather: {temp}°C, {humidity}% humidity, {condition}
        - Goal: Create 3 distinct outfits from the user's uploaded images that prioritize comfort, occasion-appropriateness, and visual harmony.

        Styling Logic:
        1. Weather Suitability: Select fabrics and layers appropriate for {temp}°C. If {condition} involves rain or wind, prioritize functional outerwear.
        2. Color Matching: Use the 60-30-10 rule for color balance. Ensure the "Stylized" option uses high-contrast complementary colors (e.g., Blue/Orange, Purple/Yellow).
        3. Harmony: Ensure shoes and accessories coordinate with the primary outfit color.

        Task: Return a JSON object containing 3 outfit suggestions:
        1. "Casual": Optimized for movement and comfort for a day out in {city}.
        2. "Work/Semi-Formal": A polished "smart-casual" or professional look that respects the current {temp}°C (e.g., blazer or knitwear if cool).
        3. "Color-Focused": A bold, high-fashion combination using complementary or triadic color schemes to make a statement.

        Output Format (STRICT JSON ONLY):
        {{
            "suggestions": [
                {{
                    "occasion": "Casual",
                    "explanation": "Briefly explain why these pieces suit {temp}°C and the chosen color palette.",
                    "outfit_ids": ["id1", "id2", "id3"]
                }},
                {{
                    "occasion": "Work",
                    "explanation": "Explain the professional appeal and weather-readiness.",
                    "outfit_ids": ["id4", "id5"]
                }},
                {{
                    "occasion": "Color-focused",
                    "explanation": "Identify the specific color theory used (e.g., complementary) and why it's visually striking.",
                    "outfit_ids": ["id6", "id7"]
                }}
            ]
        }}
        """
    
    contents = [prompt] + image_parts
    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=contents,
        config={'response_mime_type': 'application/json'}
    )
    return json.loads(response.text)
