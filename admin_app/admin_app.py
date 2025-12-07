import streamlit as st
import pandas as pd
import requests

st.set_page_config(page_title="Admin Dashboard", layout="wide")

BACKEND_URL = "https://review-system-yb2p.onrender.com"

st.title("Admin Dashboard: Submissions")
st.write("")

# -----------------------------
# LOAD SUBMISSIONS
# -----------------------------
@st.cache_data(ttl=30)
def load_submissions():
    try:
        r = requests.get(f"{BACKEND_URL}/submissions")
        if r.status_code == 200:
            return pd.json_normalize(r.json())
        return pd.DataFrame()
    except:
        return pd.DataFrame()


# -----------------------------
# LOAD STATS
# -----------------------------
def load_stats():
    try:
        r = requests.get(f"{BACKEND_URL}/stats")
        if r.status_code == 200:
            return r.json()
        return None
    except:
        return None


if st.button("Refresh"):
    st.cache_data.clear()

df = load_submissions()

# -----------------------------
# TABLE
# -----------------------------
st.subheader("All Submissions")

if df.empty:
    st.info("No data found.")
else:
    st.dataframe(
        df[["id", "rating", "review", "user_response", "summary", "actions", "created_at"]],
        use_container_width=True
    )


# -----------------------------
# STATS
# -----------------------------
st.subheader("Stats")

stats = load_stats()
if stats:
    st.write(f"**Total Reviews:** {stats['total']}")
    st.write(f"**Average Rating:** {round(stats['average_rating'], 2)}")
    st.write(f"**Distribution:** {stats['distribution']}")


# -----------------------------
# CHARTS (Plotly removed — ensure no import errors)
# -----------------------------
if not df.empty:
    st.subheader("Rating Distribution Chart")
    st.bar_chart(df["rating"].value_counts().sort_index())


if not df.empty:
    st.subheader("Submission Timeline")
    df["created_at"] = pd.to_datetime(df["created_at"])
    df_sorted = df.sort_values("created_at")
    st.line_chart(df_sorted.set_index("created_at")["id"])


# -----------------------------
# VIEW SINGLE REVIEW
# -----------------------------
st.subheader("View Detailed Review by ID")

review_id = st.text_input("Enter Review ID")

if review_id:
    try:
        r = requests.get(f"{BACKEND_URL}/submissions/{review_id}")
        if r.status_code == 200:
            st.json(r.json())
        else:
            st.error("Review not found.")
    except:
        st.error("Server error. Check backend URL.")
