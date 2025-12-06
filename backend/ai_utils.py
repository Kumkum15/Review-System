# backend/ai_utils.py
"""
AI utilities using Google Gemini (GENAPI_KEY).
If GENAPI_KEY is missing or the API fails, deterministic fallbacks are used
so the full project always remains functional.
"""

import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

GENAPI_KEY = os.getenv("GENAPI_KEY")

# Configure Gemini
if GENAPI_KEY:
    genai.configure(api_key=GENAPI_KEY)

# ------------------------
# FALLBACK FUNCTIONS
# ------------------------

def _fallback_user_response(rating: int, review: str) -> str:
    if rating >= 4:
        return "Thank you so much for your positive feedback! We're glad you had a good experience."
    elif rating == 3:
        return "Thank you for your honest feedback. We will work on improving your experience next time."
    else:
        return "We’re sorry to hear about your experience. Thank you for bringing this to our attention."

def _fallback_summary(review: str) -> str:
    review = review.strip()
    if not review:
        return "No review provided."
    if len(review) > 120:
        return review[:120] + "..."
    return review

def _fallback_actions(rating: int, review: str) -> str:
    actions = []
    if rating <= 2:
        actions.append("Reach out to the user with an apology and offer a resolution.")
        actions.append("Investigate issue internally based on review details.")
    elif rating == 3:
        actions.append("Ask user for additional feedback on what could be improved.")
        actions.append("Offer minor compensation or improvement assurance.")
    else:
        actions.append("Thank the user and encourage further engagement.")
        actions.append("Consider highlighting this review as a testimonial.")
    return " ".join(actions)

# ------------------------
# GEMINI LLM CALLER
# ------------------------

def _gemini_call(prompt: str) -> str:
    """
    Calls Gemini 1.5 Flash model.
    Returns plain text output.
    """
    try:
        model = genai.GenerativeModel("gemini-1.5-flash")
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception:
        return None  # triggers fallback


# ------------------------
# PUBLIC FUNCTIONS
# ------------------------

def generate_user_response(rating: int, review: str) -> str:
    prompt = f"""
You are a customer support AI. A user gave a rating: {rating} stars.
Their review: "{review}"

Write a friendly and helpful customer response in 2–3 lines.
"""
    if GENAPI_KEY:
        out = _gemini_call(prompt)
        if out: return out
    return _fallback_user_response(rating, review)


def generate_summary(review: str) -> str:
    prompt = f"""
Summarize this review in one short sentence:
"{review}"
"""
    if GENAPI_KEY:
        out = _gemini_call(prompt)
        if out: return out
    return _fallback_summary(review)


def generate_actions(rating: int, review: str) -> str:
    prompt = f"""
Provide 2 short recommended business actions based on:
Rating: {rating}
Review: "{review}"
Format as plain text list, no numbering needed.
"""
    if GENAPI_KEY:
        out = _gemini_call(prompt)
        if out: return out
    return _fallback_actions(rating, review)
