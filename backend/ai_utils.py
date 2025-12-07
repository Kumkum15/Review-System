# backend/ai_utils.py
import os
import requests
from dotenv import load_dotenv

load_dotenv()

# Environment variable name (set this in Render env)
API_KEY = os.getenv("GENAPI_KEY") or os.getenv("GEMINI_API_KEY")
# model name; change if needed. If your Google account uses different model, update.
MODEL = os.getenv("GEN_MODEL", "gemini-1.5")

# Use Google Generative Language REST API endpoint (v1beta)
BASE_URL_TEMPLATE = "https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={key}"

def call_gemini(prompt: str, max_output_tokens: int = 256) -> str:
    if not API_KEY:
        # Local fallback (no API key): return a simple templated reply
        return f"(dev) simulated response for prompt: {prompt[:120]}..."

    url = BASE_URL_TEMPLATE.format(model=MODEL, key=API_KEY)
    payload = {
        "temperature": 0.2,
        "candidate_count": 1,
        "max_output_tokens": max_output_tokens,
        "content_filter": {"candidates": ["BLOCK_TOO_MUCH"]},  # optional
        "prompt": {
            "messages": [
                {"role": "user", "content": [{"type": "text", "text": prompt}]}
            ]
        }
    }

    try:
        r = requests.post(url, json=payload, timeout=20)
        r.raise_for_status()
        data = r.json()
        # Extract text in possible shapes (adapt if Google response shape differs)
        if "candidates" in data and isinstance(data["candidates"], list) and data["candidates"]:
            candidate = data["candidates"][0]
            # new API shape: candidate["content"] -> parts
            if "content" in candidate:
                # candidate["content"] could be list of parts
                parts = candidate["content"].get("parts") if isinstance(candidate["content"], dict) else None
                if parts and isinstance(parts, list):
                    return "".join(p.get("text", "") for p in parts)
            # fallback
            return candidate.get("output", candidate.get("content", "")) or ""
        # Another fallback shape:
        return data.get("result", {}).get("outputs", [{}])[0].get("content", [{}])[0].get("text", "") or ""
    except Exception as e:
        return f"(AI error) {str(e)}"

def generate_user_response(rating: int, review: str) -> str:
    prompt = (
        f"You are a polite customer support assistant. User left rating {rating}/5 and wrote:\n\n"
        f"\"{review}\"\n\n"
        "Write a short empathetic response to the user (one paragraph)."
    )
    return call_gemini(prompt, max_output_tokens=120)

def generate_summary(review: str) -> str:
    prompt = f"Summarize this customer review in one short sentence:\n\n\"{review}\""
    return call_gemini(prompt, max_output_tokens=80)

def generate_actions(rating: int, review: str) -> str:
    prompt = (
        f"Based on a {rating}/5 rating and this review:\n\n\"{review}\"\n\n"
        "List 3 concise internal action items for the product/operations team."
    )
    return call_gemini(prompt, max_output_tokens=120)
