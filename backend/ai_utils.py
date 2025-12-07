import os
import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")
MODEL = os.getenv("MODEL", "gemini-1.0-pro")

BASE_URL_TEMPLATE = "https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={key}"

def call_gemini(prompt: str, max_output_tokens: int = 150) -> str:
    """
    Call Google Generative Language REST endpoint.
    IMPORTANT: Always return a STRING. Never return None.
    """
    if not API_KEY:
        return "(AI disabled – no API key provided)"

    url = BASE_URL_TEMPLATE.format(model=MODEL, key=API_KEY)
    payload = {
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {"maxOutputTokens": max_output_tokens, "temperature": 0.3}
    }

    try:
        r = requests.post(url, json=payload, timeout=20)
        r.raise_for_status()
        data = r.json()

        # safe extraction — if response shape differs, return fallback string
        try:
            return data["candidates"][0]["content"]["parts"][0]["text"] or "(AI returned empty text)"
        except Exception:
            # fallback for other shapes
            if isinstance(data, dict):
                # pick any text-like leaf we can find (best effort)
                # safe, non-crashing fallback
                return "(AI error – unexpected response shape)"
            return "(AI error – unexpected API response)"

    except Exception as e:
        return f"(AI error – {str(e)})"


def generate_user_response(rating: int, review: str) -> str:
    prompt = (
        f"You are a polite customer support assistant. User left rating {rating}/5 and wrote:\n\n"
        f"\"{review}\"\n\nWrite a short empathetic reply (one short paragraph)."
    )
    return call_gemini(prompt, max_output_tokens=120)


def generate_summary(review: str) -> str:
    prompt = f"Summarize this customer review in one short sentence:\n\n\"{review}\""
    return call_gemini(prompt, max_output_tokens=60)


def generate_actions(rating: int, review: str) -> str:
    prompt = (
        f"Based on a {rating}/5 rating and this review:\n\n\"{review}\"\n\n"
        "List 3 concise internal action items for the product/operations team."
    )
    return call_gemini(prompt, max_output_tokens=120)
