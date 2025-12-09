import requests
import time
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage

LIGHTX_API_KEY = "79708d18b10f4f8480952bcff855fcc4_f98e9f62b84446f09a2ea9113f0cea54_andoraitools"
AVATAR_URL = "https://api.lightxeditor.com/external/api/v2/avatar"
STATUS_URL = "https://api.lightxeditor.com/external/api/v2/order-status"

def generate_lightx_avatar_and_save(user, url, reference_url=None, prompt=""):
    
   
    headers = {
        'Content-Type': 'application/json',
        'x-api-key': LIGHTX_API_KEY
    }
    payload = {
        "imageUrl": url,
        "textPrompt": prompt
    }

    if reference_url:
        payload["avatarReferenceUrl"] = reference_url

    try:
        create_res = requests.post(AVATAR_URL, headers=headers, json=payload)
        create_json = create_res.json()
        if create_json.get("statusCode") != 2000:
            return {"success": False, "error": f"Avatar creation failed: {create_json}"}

        order_id = create_json["body"]["orderId"]

        for _ in range(5):
            status_res = requests.post(
                STATUS_URL,
                headers=headers,
                json={"orderId": order_id}
            )
            status_json = status_res.json()
            job_status = status_json["body"]["status"]

            if job_status == "active":
                avatar_url = status_json["body"].get("output")
                if avatar_url:
                    avatar_content = requests.get(avatar_url).content
                    avatar_name = f"avatar_{user.id}_{int(time.time())}.jpeg"
                    user.user_image.save(avatar_name, ContentFile(avatar_content), save=True)
                    return {"success": True, "avatar_url": avatar_url}
                else:
                    return {"success": False, "error": "No avatar output returned"}

            if job_status == "failed":
                return {"success": False, "error": "LightX avatar generation failed", "raw": status_json}

            time.sleep(3)

        return {"success": False, "error": "Timeout — avatar not ready after 5 attempts"}
    except Exception as e:
        return {"success": False, "error": str(e)}
    
