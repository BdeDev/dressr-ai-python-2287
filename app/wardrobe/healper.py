from google import genai
from google.genai import types
import json
import PIL.Image
import os

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = './mydressr-project-ef3d96e53e7a.json'

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

    # REINFORCED PROMPT: Using a clear mapping table for the AI
    prompt = """
        Analyze the clothing in this image. 
        Return a JSON object with these EXACT keys:
        
        1. "title": A descriptive name (e.g., "Navy Blue Summer Dress").
        2. "type": The specific garment type (e.g., "T-Shirt", "Chinos", "Sneakers").
        3. "category_id": Return ONLY the integer based on this mapping:
        - TOP = 1
        - BOTTOM = 2
        - DRESS = 3
        - JACKET = 4
        - SHOES_CAT = 5
        - GOGGLES = 6
        - PURSE = 7
        - HAT = 8
        4. "color": Main color.
        5. "occasion": Best suited occasion.
        6. "weather_type": Best suited weather.

        If you are unsure, pick the closest match. Do not return null for category_id.
    """

    config = types.GenerateContentConfig(
        response_mime_type="application/json",
        safety_settings=[
            types.SafetySetting(category="HARM_CATEGORY_SEXUALLY_EXPLICIT", threshold="BLOCK_NONE"),
        ]
    )

    response = client.models.generate_content(
        model="gemini-2.0-flash",
        config=config,
        contents=[
            types.Part.from_bytes(data=image_bytes, mime_type="image/jpeg"),
            prompt
        ]
    )

    if not response.text:
        return {"error": "No response from AI", "category_id": 0}

    return json.loads(response.text)


def normalize_ai_result(ai_data: dict) -> dict:
    """
    Ensures we get valid data and converts strings to integers if the AI makes a mistake.
    """
    def clean_str(value, default="Unknown"):
        if isinstance(value, list) and value:
            return str(value[0])
        return str(value) if value else default

    # Extract category_id and force it to be an integer
    raw_cat = ai_data.get("category_id")
    try:
        # This handles cases where AI returns "1" (string) instead of 1 (int)
        category_id = int(raw_cat)
    except (ValueError, TypeError):
        category_id = 0 # Default to 0/Unknown if parsing fails

    return {
        "title": clean_str(ai_data.get("title"), "New Clothing Item"),
        "type": clean_str(ai_data.get("type"), "Other"),
        "category_id": category_id,
        "color": clean_str(ai_data.get("color")),
        "occasion": clean_str(ai_data.get("occasion"), "Casual"),
        "weather_type": clean_str(ai_data.get("weather_type"), "All-weather"),
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
