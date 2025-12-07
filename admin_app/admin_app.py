import streamlit as st
import pandas as pd
import requests
import altair as alt
import os

st.set_page_config(page_title="Admin Dashboard", layout="wide")
st.title("Admin Dashboard: Submissions")

BACKEND = os.getenv("BACKEND_URL", "http://localhost:8000").rstrip("/")

if st.button("Refresh"):
    st.experimental_rerun()

def fetch_submissions():
    try:
        r = requests.get(f"{BACKEND}/submissions", timeout=8)
        r.raise_for_status()
        return r.json()
    except Exception as e:
        st.error(f"Could not fetch submissions from backend: {e}")
        return []

def fetch_stats():
    try:
        r = requests.get(f"{BACKEND}/stats", timeout=8)
        r.raise_for_status()
        return r.json()
    except Exception as e:
        st.error(f"Could not fetch stats from backend: {e}")
        return {"total": 0, "average_rating": 0, "distribution": {}}

data = fetch_submissions()
stats = fetch_stats()

st.header("All Submissions")
if len(data) == 0:
    st.info("No submissions yet.")
else:
    df = pd.DataFrame(data).sort_values("id", ascending=True).reset_index(drop=True)
    st.dataframe(df, hide_index=True, use_container_width=True)

st.header("Stats")
st.write(f"**Total Reviews:** {stats.get('total', 0)}")
st.write(f"**Average Rating:** {round(stats.get('average_rating', 0),2)}")
st.write(f"**Distribution:** {stats.get('distribution', {})}")

st.subheader("Rating Distribution Chart")
dist = stats.get("distribution", {})
if dist:
    chart_df = pd.DataFrame({"rating": list(dist.keys()), "count": list(dist.values())})
    chart = (alt.Chart(chart_df).mark_bar().encode(x=alt.X("rating:N", title="Rating"), y=alt.Y("count:Q", title="Count"), tooltip=["rating","count"]).properties(height=300))
    st.altair_chart(chart, use_container_width=True)
