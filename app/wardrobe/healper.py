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
        Weather for {city}: {temp}°C, {humidity}% humidity, {condition}.
        
        Task: Provide 3 different outfit suggestions from the provided images.
        1. Casual: Comfortable for daily wear in this weather.
        2. Semi-Formal/Work: Polished but weather-appropriate.
        3. Stylized/Color-Focused: A bold combination based on complementary colors.

        Return ONLY a JSON object with this structure:
        {{
            "suggestions": [
                {{
                    "occasion": "Casual",
                    "explanation": "why this works",
                    "outfit_ids": [ids]
                }},
                {{
                    "occasion": "Work",
                    "explanation": "why this works",
                    "outfit_ids": [ids]
                }},
                {{
                    "occasion": "Color-focused",
                    "explanation": "why this works",
                    "outfit_ids": [ids]
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
