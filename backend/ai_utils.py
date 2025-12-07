import requests

HF_URL = "https://api-inference.huggingface.co/models/meta-llama/Llama-3.1-8B-Instruct"

def call_ai(prompt: str, max_tokens: int = 150):
    payload = {
        "inputs": prompt,
        "parameters": {"max_new_tokens": max_tokens}
    }

    try:
        r = requests.post(HF_URL, json=payload, timeout=20)
        r.raise_for_status()
        data = r.json()

        if isinstance(data, list) and "generated_text" in data[0]:
            return data[0]["generated_text"]

        return "(AI) unexpected response"
    except Exception as e:
        return f"(AI error) {str(e)}"


def generate_user_response(rating: int, review: str) -> str:
    prompt = (
        f"You are a polite customer support assistant. "
        f"The user gave rating {rating}/5 and wrote:\n\n"
        f"\"{review}\"\n\n"
        "Write a warm, short message under the heading 'We are listening'."
    )
    return call_ai(prompt)


def generate_summary(review: str) -> str:
    prompt = f"Summarize this customer review in one short sentence:\n\n{review}"
    return call_ai(prompt, 60)


def generate_actions(rating: int, review: str) -> str:
    prompt = (
        f"Based on rating {rating}/5 and the review:\n\n{review}\n\n"
        "List 3 internal action items for the team."
    )
    return call_ai(prompt)
