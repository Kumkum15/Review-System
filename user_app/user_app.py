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

    # Validation
    if rating is None or review_text.strip() == "":
        st.error("Please provide both rating and review.")
    else:
        payload = {"rating": rating, "review": review_text}

        try:
            r = requests.post(f"{BACKEND}/submit", json=payload)

            if r.status_code == 200:
                result = r.json()

                # Success Message
                st.success("Thanks!! Your review matters a lot!", icon="💚")

                # === AI RESPONSE BOX ===
                st.markdown("### ❤️ We're Listening")
                st.info(result.get("user_response", "No AI response"))

            else:
                st.error("Server error. Please try again later.")

        except Exception as e:
            st.error(f"Network error: {str(e)}")
