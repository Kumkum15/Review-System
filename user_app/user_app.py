import streamlit as st
import requests
import os

st.set_page_config(page_title="Leave a Review", layout="wide")
st.title("Leave a Review")

BACKEND = os.getenv("BACKEND_URL", "http://localhost:8000").rstrip("/")

rating = st.radio("Rating", [5,4,3,2,1], index=4, horizontal=False)
review = st.text_area("Write your review", height=150)

if st.button("Submit Review"):
    if not review.strip():
        st.error("Please write a short review.")
    else:
        payload = {"rating": rating, "review": review}
        try:
            r = requests.post(f"{BACKEND}/submit", json=payload, timeout=10)
            if r.status_code == 200:
                st.success("Thanks!! Your review matters a lot!")
                data = r.json()
                st.markdown("### We're Listening ❤️")
                st.write(data.get("user_response", "(none)"))
                st.markdown("**AI summary:**")
                st.write(data.get("summary", "(none)"))
                st.markdown("**AI action items:**")
                st.write(data.get("actions", "(none)"))
            else:
                st.error("Something went wrong. Please try again.")
                st.write(r.text)
        except Exception as e:
            st.error(f"Could not reach backend: {str(e)}")
