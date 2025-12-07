import streamlit as st
import pandas as pd
import requests
import os

st.set_page_config(page_title="Admin Dashboard", layout="wide")
BACKEND = os.getenv("BACKEND_URL", "http://localhost:8000").rstrip("/")

st.title("Admin Dashboard: Submissions")

if st.button("Refresh"):
    st.experimental_rerun()

def fetch_submissions():
    try:
        r = requests.get(f"{BACKEND}/submissions", timeout=10)
        r.raise_for_status()
        return r.json()
    except Exception as e:
        st.error(f"Could not fetch submissions: {e}")
        return []

def fetch_stats():
    try:
        r = requests.get(f"{BACKEND}/stats", timeout=10)
        r.raise_for_status()
        return r.json()
    except Exception as e:
        st.error(f"Could not fetch stats: {e}")
        return {"total": 0, "average_rating": 0, "distribution": {}}

data = fetch_submissions()
stats = fetch_stats()

st.header("All Submissions")
if not data:
    st.info("No submissions yet.")
else:
    df = pd.DataFrame(data).sort_values(by="id", ascending=True).reset_index(drop=True)
    st.dataframe(df, use_container_width=True)

st.header("Stats")
st.write(f"**Total Reviews:** {stats.get('total', 0)}")
st.write(f"**Average Rating:** {round(stats.get('average_rating', 0.0), 2)}")
st.write(f"**Distribution:** {stats.get('distribution', {})}")

# rating chart
if stats.get("distribution"):
    chart_df = pd.DataFrame({
        "rating": list(stats["distribution"].keys()),
        "count": list(stats["distribution"].values()),
    })
    st.bar_chart(chart_df.set_index("rating"))
