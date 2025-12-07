import streamlit as st
import os
import requests

BACKEND = os.getenv("BACKEND_URL", "http://localhost:8000").rstrip("/")

st.set_page_config(page_title="Leave a Review", layout="centered")
st.title("Leave a Review")

rating = st.radio("Rating", [5,4,3,2,1])
review = st.text_area("Write your review", height=140)

if st.button("Submit Review"):
    payload = {"rating": int(rating), "review": review}
    try:
        r = requests.post(f"{BACKEND}/submit", json=payload, timeout=15)
        if r.status_code == 200:
            st.success("Thanks!! Your review matters a lot!")
            res = r.json()
            st.write("AI response:", res.get("user_response"))
            st.write("Summary:", res.get("summary"))
            st.write("Actions:", res.get("actions"))
        else:
            st.error(f"Something went wrong. ({r.status_code}) {r.text}")
    except Exception as e:
        st.error(f"Internal Server Error: {e}")
