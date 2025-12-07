import os
import requests
from dotenv import load_dotenv

load_dotenv()

# Get API key
API_KEY = os.getenv("GEMINI_API_KEY")

# Use a VALID Google REST model name
MODEL = os.getenv("GEN_MODEL", "gemini-1.5-flash")

# Correct REST API endpoint
BASE_URL_TEMPLATE = (
    "https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={key}"
)

def call_gemini(prompt: str, max_output_tokens: int = 256) -> str:
    if not API_KEY:
        return f"(AI disabled) No API key found • prompt: {prompt[:80]}..."

    url = BASE_URL_TEMPLATE.format(model=MODEL, key=API_KEY)

    # Correct v1beta REST payload format
    payload = {
        "contents": [
            {
                "role": "user",
                "parts": [
                    {"text": prompt}
                ]
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

        # correct extraction for REST API
        return data["candidates"][0]["content"]["parts"][0]["text"]

    except Exception as e:
        return f"(AI error) {str(e)}"


def generate_user_response(rating: int, review: str) -> str:
    prompt = (
        f"You are a polite customer support assistant.\n"
        f"User rated {rating}/5 and wrote:\n\n"
        f"\"{review}\".\n\n"
        f"Write a short empathetic reply."
    )
    return call_gemini(prompt, max_output_tokens=120)


def generate_summary(review: str) -> str:
    return call_gemini(
        f"Summarize this customer review in one short sentence:\n\"{review}\"",
        max_output_tokens=60
    )


def generate_actions(rating: int, review: str) -> str:
    prompt = (
        f"Based on rating {rating}/5 and review:\n\"{review}\",\n"
        "give 3 short improvement action items."
    )
    return call_gemini(prompt, max_output_tokens=100)
