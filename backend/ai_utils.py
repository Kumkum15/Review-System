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
    if not API_KEY:
        return "(AI error) No API key found."

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

        # VERY IMPORTANT FIX
        return data["candidates"][0]["content"]["parts"][0]["text"]

    except Exception as e:
        return f"(AI error) {str(e)}"


# ---------------------------------------------------------
# REQUIRED FUNCTIONS FOR MAIN.PY
# ---------------------------------------------------------

def generate_user_response(rating: int, review: str) -> str:
    prompt = f"""
You are a polite customer support agent.
Customer rating: {rating}/5
Review: {review}

Write a short, friendly reply to the customer.
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
Given the customer rating ({rating}/5) and review below, suggest 1–2 action items for the company:

Review: {review}
"""
    return call_gemini(prompt)
