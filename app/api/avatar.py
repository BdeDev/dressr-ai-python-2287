import requests
from accounts.utils import get_api_key

LIGHTX_API_KEY = get_api_key()
CHECK_STATUS = "https://api.lightxeditor.com/external/api/v2/order-status"

def create_lightx_avatar(image_url: str, reference_url: str = None, prompt: str = ""):
    url = "https://api.lightxeditor.com/external/api/v2/avatar"
    headers = {
        "Content-Type": "application/json",
        "x-api-key": LIGHTX_API_KEY
    }
    payload = {"imageUrl": image_url}
    if reference_url:
        payload["avatarReferenceUrl"] = reference_url
    if prompt:
        payload["textPrompt"] = prompt

    try:
        response = requests.post(url, headers=headers, json=payload)
        return {"success": True, "data": response.json()} if response.status_code == 200 else {
            "success": False,
            "status_code": response.status_code,
            "error": response.text
        }
    except Exception as e:
        return {"success": False, "error": str(e)}


def check_lightx_order_status(order_id: str):

    url = CHECK_STATUS
    headers = {
        "Content-Type": "application/json",
        "x-api-key": LIGHTX_API_KEY
    }
    payload = {"orderId": order_id}
    try:
        response = requests.post(url, headers=headers, json=payload)
        return {"success": True, "data": response.json()} if response.status_code == 200 else {
            "success": False,
            "status_code": response.status_code,
            "error": response.text
        }
    except Exception as e:
        return {"success": False, "error": str(e)}
    

def lightx_virtual_tryon(image_url: str, style_image_url: str, segmentation_type: int):
    headers = {
        "Content-Type": "application/json",
        "x-api-key": LIGHTX_API_KEY
    }
    START_JOB_URL = 'https://api.lightxeditor.com/external/api/v2/aivirtualtryon'
    payload = {
        "imageUrl": image_url,
        "styleImageUrl": style_image_url,
        "segmentationType": segmentation_type     # 0 for Upper Body, 1 for Lower body, 2 for Full body
    }
    try:
        response = requests.post(START_JOB_URL, headers=headers, json=payload)
        data = response.json()
        return {"success": True, "data": response.json()} if response.status_code == 200 else {
            "success": False,
            "status_code": response.status_code,
            "error": response.text
        }
    except Exception as e:
        return {"success": False, "error": str(e)}
    
def check_virtual_tryon_status(order_id):
    headers = {
        "Content-Type": "application/json",
        "x-api-key": LIGHTX_API_KEY
    }
    status_url = CHECK_STATUS
    payload = {"orderId": order_id}

    try:
        response = requests.post(status_url, headers=headers, json=payload)
        return {"success": True, "data": response.json()} if response.status_code == 200 else {
            "success": False,
            "status_code": response.status_code,
            "error": response.text
        }
    except Exception as e:
        return {"success": False, "error": str(e)}



def create_lightx_outfit(image_url: str, prompt: str = ""):
    url = "https://api.lightxeditor.com/external/api/v2/outfit"
    headers = {
        "Content-Type": "application/json",
        "x-api-key": LIGHTX_API_KEY
    }
    payload = {
        "imageUrl": image_url,
        "textPrompt": prompt
        }
    try:
        response = requests.post(url, headers=headers, json=payload)
        return {"success": True, "data": response.json()} if response.status_code == 200 else {
            "success": False,
            "status_code": response.status_code,
            "error": response.text
        }
    except Exception as e:
        return {"success": False, "error": str(e)}
    

    
def check_outfit_status(order_id):
    headers = {
        "Content-Type": "application/json",
        "x-api-key": LIGHTX_API_KEY
    }
    status_url = CHECK_STATUS
    payload = {"orderId": order_id}

    try:
        response = requests.post(status_url, headers=headers, json=payload)
        return {"success": True, "data": response.json()} if response.status_code == 200 else {
            "success": False,
            "status_code": response.status_code,
            "error": response.text
        }
    except Exception as e:
        return {"success": False, "error": str(e)}