import streamlit as st
import pandas as pd
import requests
import altair as alt
import os

st.set_page_config(page_title="Admin Dashboard", layout="wide")

BACKEND = os.getenv("BACKEND_URL", "http://localhost:8000")

st.title("Admin Dashboard: Submissions")

# Refresh button
if st.button("Refresh"):
    st.rerun()

# -----------------------------
# Fetch Data
# -----------------------------
def fetch_submissions():
    try:
        r = requests.get(f"{BASE_URL}/submissions")
        return r.json()
    except:
        st.error("Could not fetch submissions from backend.")
        return []

def fetch_stats():
    try:
        r = requests.get(f"{BASE_URL}/stats")
        return r.json()
    except:
        st.error("Could not fetch stats.")
        return {"total": 0, "average_rating": 0, "distribution": {}}

data = fetch_submissions()
stats = fetch_stats()

# -----------------------------
# 1️ ALL SUBMISSIONS
# -----------------------------
st.header("All Submissions")

if len(data) == 0:
    st.info("No submissions yet.")
else:
    df = pd.DataFrame(data)

    # Sort by ID ASC
    df = df.sort_values(by="id", ascending=True).reset_index(drop=True)

    st.dataframe(df, hide_index=True, use_container_width=True)

# -----------------------------
# 2️ STATS SECTION
# -----------------------------
st.header("Stats")

st.write(f"**Total Reviews:** {stats['total']}")
st.write(f"**Average Rating:** {round(stats['average_rating'], 2)}")
st.write(f"**Distribution:** {stats['distribution']}")

# -----------------------------
# 3️ GRAPHS
# -----------------------------

# Rating Distribution Chart
st.subheader("Rating Distribution Chart")

if stats["distribution"]:
    chart_df = pd.DataFrame({
        "rating": list(stats["distribution"].keys()),
        "count": list(stats["distribution"].values()),
    })

    bar_chart = (
        alt.Chart(chart_df)
        .mark_bar()
        .encode(
            x=alt.X("rating:N", title="Rating"),
            y=alt.Y("count:Q", title="Count"),
            tooltip=["rating", "count"],
        )
        .properties(height=300)
    )

    st.altair_chart(bar_chart, use_container_width=True)

# Timeline Graph
if len(data):
    st.subheader("Submission Timeline")

    df_t = df[["id", "created_at"]].copy()
    df_t["created_at"] = pd.to_datetime(df_t["created_at"])

    timeline = (
        alt.Chart(df_t)
        .mark_line(point=True)
        .encode(
            x=alt.X("created_at:T", title="Date & Time"),
            y=alt.Y("id:Q", title="Review ID"),
            tooltip=["id", "created_at"],
        )
        .properties(height=300)
    )

    st.altair_chart(timeline, use_container_width=True)

# -----------------------------
# 4️ VIEW DETAILED REVIEW
# -----------------------------
st.header("View Detailed Review by ID")

review_id = st.text_input("Enter Review ID")

if review_id:
    try:
        review_id = int(review_id)
        df_lookup = pd.DataFrame(data)

        match = df_lookup[df_lookup["id"] == review_id]

        if len(match):
            st.subheader("Detailed Review")
            st.json(match.to_dict(orient="records")[0])
        else:
            st.error("No review found with this ID.")
    except:
        st.error("Please enter a valid numeric ID.")
