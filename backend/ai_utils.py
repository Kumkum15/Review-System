# backend/ai_utils.py
import os
import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")
MODEL = "gemini-1.0-pro"

BASE_URL_TEMPLATE = (
    "https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={key}"
)

def call_gemini(prompt: str, max_output_tokens: int = 150) -> str:
    """Always return a STRING. Never return None."""
    
    # No API Key – return safe fallback
    if not API_KEY:
        return "(AI disabled – no API key found)"

    url = BASE_URL_TEMPLATE.format(model=MODEL, key=API_KEY)

    payload = {
        "contents": [
            {"parts": [{"text": prompt}]}
        ],
        "generationConfig": {
            "maxOutputTokens": max_output_tokens,
            "temperature": 0.3
        }
    }

    try:
        r = requests.post(url, json=payload, timeout=20)
        r.raise_for_status()
        data = r.json()

        # SAFELY extract text
        try:
            return data["candidates"][0]["content"]["parts"][0]["text"]
        except:
            return "(AI error – unexpected API response)"

    except Exception as e:
        # ALWAYS return a string, NEVER None
        return f"(AI error – {str(e)})"


def generate_user_response(rating: int, review: str) -> str:
    prompt = (
        f"You are a polite assistant. User rated {rating}/5 and wrote:\n"
        f"\"{review}\"\nWrite a short friendly reply."
    )
    return call_gemini(prompt)


def generate_summary(review: str) -> str:
    return call_gemini(f"Summarize this review in one short line: \"{review}\"")


def generate_actions(rating: int, review: str) -> str:
    prompt = (
        f"User rating: {rating}/5\nReview: \"{review}\"\n"
        "Give 3 short improvement actions."
    )
    return call_gemini(prompt)
