import os
import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")
MODEL = "gemini-1.0-pro"   # FINAL FIX – WORKS WITH generateContent

BASE_URL_TEMPLATE = (
    "https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={key}"
)

def call_gemini(prompt: str, max_output_tokens: int = 256) -> str:
    if not API_KEY:
        return f"(AI disabled) No API key found • prompt: {prompt[:80]}..."

    url = BASE_URL_TEMPLATE.format(model=MODEL, key=API_KEY)

    payload = {
        "contents": [
            {
                "parts": [{"text": prompt}]
            }
        ],
        "generationConfig": {
            "maxOutputTokens": max_output_tokens,
            "temperature": 0.2
        }
    }

    try:
        r = requests.post(url, json=payload, timeout=20)
        r.raise_for_status()
        data = r.json()
        return data["candidates"][0]["content"]["parts"][0]["text"]

    except Exception as e:
        return f"(AI error) {str(e)}"
