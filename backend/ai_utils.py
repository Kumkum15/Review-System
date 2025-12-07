import os
import requests
from dotenv import load_dotenv
load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")  # set this on Render (or .env locally)
MODEL = os.getenv("GEN_MODEL", "gemini-1.5-flash")

BASE_URL_TEMPLATE = "https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={key}"

def _safe_return(val: str) -> str:
    if val is None:
        return "(AI error) no response"
    if isinstance(val, str) and val.strip() == "":
        return "(AI) empty response"
    return str(val)

def call_gemini(prompt: str, max_output_tokens: int = 150) -> str:
    # If no API key, return fallback string immediately
    if not API_KEY:
        return f"(AI disabled) no API key • prompt start: {prompt[:80]}..."

    url = BASE_URL_TEMPLATE.format(model=MODEL, key=API_KEY)

    payload = {
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {
            "maxOutputTokens": max_output_tokens,
            "temperature": 0.2
        }
    }

    try:
        r = requests.post(url, json=payload, timeout=20)
        r.raise_for_status()
        data = r.json()

        # robust extraction from common response shapes
        if "candidates" in data and isinstance(data["candidates"], list) and data["candidates"]:
            cand = data["candidates"][0]
            # candidate.content.parts -> text
            if isinstance(cand.get("content"), dict):
                parts = cand["content"].get("parts")
                if isinstance(parts, list) and parts:
                    return _safe_return("".join(str(p.get("text","")) for p in parts))
            # fallback keys
            if cand.get("output"):
                return _safe_return(cand.get("output"))
            if cand.get("content"):
                return _safe_return(str(cand.get("content")))
        # final fallback: try some other shapes
        if "result" in data:
            try:
                return _safe_return(data["result"]["outputs"][0]["content"][0]["text"])
            except Exception:
                pass

        return "(AI) unexpected response shape"
    except requests.exceptions.HTTPError as e:
        # return readable error, not None
        return f"(AI error) HTTP {r.status_code} - {r.text[:200]}"
    except Exception as e:
        return f"(AI error) {str(e)}"

def generate_user_response(rating: int, review: str) -> str:
    prompt = (
        f"You are a polite customer support assistant. The user left rating {rating}/5 and wrote:\n\n"
        f"\"{review}\"\n\n"
        "Write a short empathetic response in one paragraph."
    )
    return call_gemini(prompt, max_output_tokens=120)

def generate_summary(review: str) -> str:
    prompt = f"Summarize this customer review in one short sentence:\n\n\"{review}\""
    return call_gemini(prompt, max_output_tokens=60)

def generate_actions(rating: int, review: str) -> str:
    prompt = (
        f"Based on rating {rating}/5 and this review:\n\n\"{review}\"\n\n"
        "List 3 concise internal action items."
    )
    return call_gemini(prompt, max_output_tokens=120)
