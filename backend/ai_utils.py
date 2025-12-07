import os
import requests
from dotenv import load_dotenv

load_dotenv()

# Read API Key
API_KEY = os.getenv("GENAPI_KEY") or os.getenv("GEMINI_API_KEY")

# Default model
MODEL = os.getenv("GEN_MODEL", "gemini-1.5-flash")

# Correct Google REST endpoint
BASE_URL = f"https://generativelanguage.googleapis.com/v1beta/models/{MODEL}:generateContent?key={API_KEY}"


def call_gemini(prompt: str, max_output_tokens: int = 256) -> str:
    """
    Calls Google Gemini REST API with correct request format.
    """

    if not API_KEY:
        return f"(dev mode) No API key found. Prompt: {prompt[:100]}..."

    # --- CORRECT PAYLOAD STRUCTURE FOR GEMINI ---
    payload = {
        "generationConfig": {
            "temperature": 0.4,
            "maxOutputTokens": max_output_tokens
        },
        "contents": [
            {
                "role": "user",
                "parts": [{"text": prompt}]
            }
        ]
    }

    try:
        response = requests.post(BASE_URL, json=payload, timeout=20)
        response.raise_for_status()
        data = response.json()

        # --- CORRECT RESPONSE PARSING ---
        try:
            return data["candidates"][0]["content"]["parts"][0]["text"]
        except:
            return str(data)

    except Exception as e:
        return f"(AI error) {str(e)}"


# -------------------------------------------------------------------
# HELPER FUNCTIONS FOR USER APP
# -------------------------------------------------------------------

def generate_user_response(rating: int, review: str) -> str:
    prompt = (
        f"You are a polite customer support assistant.\n"
        f"The user gave a rating of **{rating}/5**.\n\n"
        f"Review: \"{review}\"\n\n"
        f"Write a warm, empathetic 2–3 sentence response."
    )
    return call_gemini(prompt, max_output_tokens=120)


def generate_summary(review: str) -> str:
    prompt = (
        "Summarize the following customer review in one sentence:\n\n"
        f"\"{review}\""
    )
    return call_gemini(prompt, max_output_tokens=60)


def generate_actions(rating: int, review: str) -> str:
    prompt = (
        f"Based on rating {rating}/5 and this review:\n\n"
        f"\"{review}\"\n\n"
        "Give 3 short, actionable improvements for the internal team."
    )
    return call_gemini(prompt, max_output_tokens=120)
