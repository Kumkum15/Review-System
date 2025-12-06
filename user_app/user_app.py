import streamlit as st
import requests
import os

st.set_page_config(page_title="Leave a Review", layout="centered")

BACKEND = os.getenv("BACKEND_URL", "http://localhost:8000")

st.title("Leave a Review")

# Rating (no default selection)
rating = st.radio(
    "Rating",
    [5, 4, 3, 2, 1],
    index=None,
    horizontal=False
)

review = st.text_area("Write your review", placeholder="Type your review here...")

if st.button("Submit Review"):
    if rating is None:
        st.error("Please select a rating.")
    elif not review.strip():
        st.error("Please write a review before submitting.")
    else:
        r = requests.post(f"{BACKEND}/submit", json={"rating": rating, "review": review})
        if r.status_code == 200:
            data = r.json()
            st.success("Thanks!! Your review matters a lot!")

            st.subheader("We're Listening ❤️")
            st.write(data["user_response"])
        else:
            st.error("Something went wrong. Please try again.")
