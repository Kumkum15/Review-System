import streamlit as st
import requests

BACKEND = "https://review-system-yb2p.onrender.com"

st.title("Leave a Review")

rating = st.radio("Rating", [5, 4, 3, 2, 1], index=None)

review_text = st.text_area("Write your review")

if st.button("Submit Review"):
    if rating is None or review_text.strip() == "":
        st.error("Please provide both rating and review.")
    else:
        payload = {"rating": rating, "review": review_text}
        try:
            r = requests.post(f"{BACKEND}/submit", json=payload)
            r.raise_for_status()
            st.success("Thanks!! Your review matters a lot!")
        except Exception as e:
            st.error(str(e))

if r.status_code == 200:
    result = r.json()
    st.success("Thanks!! Your review matters a lot!", icon="💚")

    # show AI response in a styled box
    st.markdown("""
        ### ❤️ We're Listening  
    """)

    st.info(result.get("user_response", ""))
