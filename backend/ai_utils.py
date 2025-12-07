# backend/ai_utils.py

import requests
import html

HF_MODEL_URL = "https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct-v0.3"

# ------------------------------------------------
# FALLBACK (ALWAYS WORKS)
# ------------------------------------------------
def _local_user_response(rating: int, review: str) -> str:
    review = review.strip()
    if rating >= 4:
        return "Thank you so much for your positive feedback! We're glad you had a great experience."
    if rating == 3:
        return "Thank you for your feedback. We’ll use your input to improve your experience."
    return "We're sorry you had a poor experience. Thanks for telling us — we'll work to improve."

def _local_summary(review: str) -> str:
    if not review.strip():
        return "No review text provided."
    return review.split(".")[0][:150]

def _local_actions(rating: int, review: str) -> str:
    if rating >= 4:
        actions = [
            "Share appreciation with the team.",
            "Highlight positive feedback during review.",
            "Encourage user to return again."
        ]
    elif rating == 3:
        actions = [
            "Request more details from user.",
            "Identify improvement areas.",
            "Monitor for repeated similar feedback."
        ]
    else:
        actions = [
            "Investigate the issue reported.",
            "Follow up with the user for details.",
            "Create an action plan for improvement."
        ]
    return "\n".join(f"- {a}" for a in actions)

# ------------------------------------------------
# HUGGINGFACE CALL
# ------------------------------------------------
def _hf_generate(prompt: str) -> str:
    """Try HuggingFace free inference. If it fails, return None."""
    try:
        response = requests.post(
            HF_MODEL_URL,
            json={"inputs": prompt},
            timeout=25
        )

        if response.status_code != 200:
            return None

        data = response.json()
        text = data[0]["generated_text"]
        return html.unescape(text)
    except:
        return None

# ------------------------------------------------
# PUBLIC FUNCTIONS USED BY BACKEND
# ------------------------------------------------
def generate_user_response(rating: int, review: str) -> str:
    prompt = (
        f"User rating: {rating}/5\n"
        f"Review: \"{review}\"\n\n"
        "Write a short, empathetic customer support response in one paragraph."
    )
    out = _hf_generate(prompt)
    return out or _local_user_response(rating, review)

def generate_summary(review: str) -> str:
    prompt = (
        f"Summarize the following review in ONE short sentence:\n\n"
        f"\"{review}\""
    )
    out = _hf_generate(prompt)
    return out or _local_summary(review)

def generate_actions(rating: int, review: str) -> str:
    prompt = (
        f"Rating: {rating}/5\n"
        f"Review: \"{review}\"\n\n"
        "List 3 short internal action items to improve business quality."
    )
    out = _hf_generate(prompt)
    return out or _local_actions(rating, review)
