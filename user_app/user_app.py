import streamlit as st
import requests

BACKEND = "https://review-system-yb2p.onrender.com"

st.title("Leave a Review")

# Rating 5 → 1
rating = st.radio("Rating", [5, 4, 3, 2, 1], index=None)

review_text = st.text_area("Write your review")

# ---------------------------------------------------
# Submit Button
# ---------------------------------------------------
if st.button("Submit Review"):
    
    if rating is None or review_text.strip() == "":
        st.error("Please provide both rating and review.")
    else:
        payload = {"rating": rating, "review": review_text}
        res = requests.post(f"{BACKEND}/submit", json=payload)

        if res.status_code == 200:
            data = res.json()
            ai_response = data["user_response"]   # only AI response

            st.success("Thanks!! Your review matters a lot!")

            st.subheader("❤️ We're Listening")
            st.info(ai_response)
        else:
            st.error("Something went wrong.")
