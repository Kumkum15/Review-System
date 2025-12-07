import os
import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")
MODEL = "gemini-1.0-pro"

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


# ---------------------------------------------------
# REQUIRED FUNCTIONS (YOUR MAIN.PY DEPENDS ON THESE)
# ---------------------------------------------------

def generate_user_response(rating: int, review: str) -> str:
    prompt = f"""
    Write a short friendly reply to this customer review.
    Rating: {rating}
    Review: {review}
    Keep the tone positive and simple.
    """
    return call_gemini(prompt)

def generate_summary(review: str) -> str:
    prompt = f"""
    Summarize this customer review in one short sentence:
    {review}
    """
    return call_gemini(prompt)

def generate_actions(rating: int, review: str) -> str:
    prompt = f"""
    Based on the customer's rating ({rating}) and review:
    "{review}"

    Suggest 2 improvement actions for the business.
    """
    return call_gemini(prompt)
