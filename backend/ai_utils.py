import os
import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")
MODEL = "gemini-pro"   # ✅ correct model for generateContent

BASE_URL_TEMPLATE = (
    "https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={key}"
)

def call_gemini(prompt: str, max_output_tokens: int = 256) -> str:
    if not API_KEY:
        return f"(AI disabled) No API key found • prompt: {prompt[:80]}..."

    url = BASE_URL_TEMPLATE.format(model=MODEL, key=API_KEY)

    payload = {
        "contents": [
            {"parts": [{"text": prompt}]}
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
        print("❌ GEMINI ERROR:", str(e))
        try:
            print("❌ RAW RESPONSE:", r.text)
        except:
            pass
        return "(AI error)"



def generate_user_response(rating: int, review: str) -> str:
    prompt = f"""
    Write a short friendly reply to this customer review.
    Rating: {rating}
    Review: {review}
    Keep the tone polite and simple.
    """
    return call_gemini(prompt)


def generate_summary(review: str) -> str:
    prompt = f"Summarize this customer review in one short sentence:\n{review}"
    return call_gemini(prompt)


def generate_actions(rating: int, review: str) -> str:
    prompt = f"""
    Based on rating {rating}/5 and review "{review}", 
    suggest 2 improvement action items.
    """
    return call_gemini(prompt)
