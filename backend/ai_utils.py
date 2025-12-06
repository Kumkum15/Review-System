import os
import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")
MODEL = "gemini-1.5-flash"

BASE_URL = f"https://generativelanguage.googleapis.com/v1beta/models/{MODEL}:generateContent?key={API_KEY}"

def call_gemini(prompt):
    body = {
        "contents": [
            {"parts": [{"text": prompt}]}
        ]
    }
    response = requests.post(BASE_URL, json=body)
    data = response.json()

    try:
        return data["candidates"][0]["content"]["parts"][0]["text"]
    except:
        return "AI Error: Unable to generate response."


def generate_user_response(rating, review):
    prompt = f"User left rating {rating} and review: '{review}'. Write a polite human–like response."
    return call_gemini(prompt)


def generate_summary(review):
    prompt = f"Summarize this review in one sentence: '{review}'"
    return call_gemini(prompt)


def generate_actions(rating, review):
    prompt = f"Based on rating {rating} and review '{review}', suggest internal business improvement actions."
    return call_gemini(prompt)
