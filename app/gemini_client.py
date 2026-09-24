import base64
import requests
from pathlib import Path
from .config import GEMINI_API_KEY

API_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-3.5-flash:generateContent"

class GeminiError(Exception):
    """Exception raised for API errors."""
    pass

def _load_image_base64(image_path: Path) -> str:
    with open(image_path, "rb") as f:
        return base64.b64encode(f.read()).decode("utf-8")

def analyze_image(image_path: Path, prompt: str) -> str:
    """Sends a screenshot and prompt to the Gemini Vision model."""
    if not GEMINI_API_KEY:
        raise GeminiError("GEMINI_API_KEY not found in .env")

    payload = {
        "contents": [{
            "role": "user", 
            "parts": [
                {"text": prompt},
                {"inlineData": {"mimeType": "image/png", "data": _load_image_base64(image_path)}}
            ]
        }]
    }
    
    response = requests.post(
        API_URL, 
        params={"key": GEMINI_API_KEY}, 
        headers={"Content-Type": "application/json"}, 
        json=payload
    )
    
    if response.status_code != 200:
        raise GeminiError(f"API Error {response.status_code}: {response.text}")
        
    try:
        return response.json()["candidates"][0]["content"]["parts"][0]["text"].strip()
    except Exception as e:
        raise GeminiError(f"Response parsing failed: {e}")
