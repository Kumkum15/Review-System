import streamlit as st
import pandas as pd
import requests
import plotly.express as px

# -------------------------------
# BACKEND URL
# -------------------------------
BACKEND_URL = "https://review-system-yb2p.onrender.com"   # ← your backend API


st.set_page_config(page_title="Admin Dashboard", layout="wide")

st.title("Admin Dashboard: Submissions")
st.write("")

# -------------------------------
# LOAD ALL SUBMISSIONS
# -------------------------------
@st.cache_data(ttl=30)
def load_submissions():
    try:
        r = requests.get(f"{BACKEND_URL}/submissions")
        if r.status_code == 200:
            return pd.json_normalize(r.json())
        return pd.DataFrame()
    except:
        return pd.DataFrame()

# -------------------------------
# LOAD STATS
# -------------------------------
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

# -------------------------------
# SHOW DATA TABLE
# -------------------------------
st.subheader("All Submissions")

if df.empty:
    st.info("No data found.")
else:
    st.dataframe(
        df[["id", "rating", "review", "user_response", "summary", "actions"]],
        use_container_width=True
    )

# -------------------------------
# STATS SECTION
# -------------------------------
st.subheader("Stats")

stats = load_stats()
if stats:
    st.write(f"**Total Reviews:** {stats['total']}")
    st.write(f"**Average Rating:** {round(stats['average_rating'], 2)}")
    st.write(f"**Distribution:** {stats['distribution']}")

# -------------------------------
# RATING DISTRIBUTION CHART
# -------------------------------
if not df.empty:
    st.subheader("Rating Distribution Chart")

    fig = px.histogram(
        df,
        x="rating",
        nbins=5,
        title="Rating Distribution",
        labels={"rating": "Rating", "count": "Count"}
    )
    st.plotly_chart(fig, use_container_width=True)

# -------------------------------
# SUBMISSION TIMELINE
# -------------------------------
if not df.empty:
    st.subheader("Submission Timeline")

    df["created_at"] = pd.to_datetime(df["created_at"])

    fig2 = px.line(
        df.sort_values("created_at"),
        x="created_at",
        y="id",
        markers=True,
        title="Submission Timeline"
    )
    st.plotly_chart(fig2, use_container_width=True)


# -------------------------------
# VIEW DETAILED REVIEW BY ID
# -------------------------------
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
        st.error("Server error.")
