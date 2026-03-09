import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

# 1. SETUP & DATA LOADING
st.set_page_config(page_title="EXFO Cluster Tracker", layout="wide")
url = "https://docs.google.com/spreadsheets/d/16WPfC7PG61knqE0xVQNg8k9Hnx3PhPbuziM9VN4Qv14/edit#gid=0"

conn = st.connection("gsheets", type=GSheetsConnection)
df = conn.read(spreadsheet=url)

# 2. THE "HIDDEN API" LOGIC (Future Scope)
# If vendor calls: your-app.streamlit.app/?api=true
if st.query_params.get("api") == "true":
    st.write(df.to_json(orient="records"))
    st.stop() # Stops rendering the UI, just returns the data

# 3. THE FANCY UI
st.title("📡 EXFO Cluster Master Tracker")
st.markdown("---")

# Metrics for the 'Fancy' look
c1, c2, c3 = st.columns(3)
c1.metric("Active Clusters", df['Parent Cluster'].nunique())
c2.metric("Total Nodes", len(df))
c3.metric("Sync Status", "✅ Live")

# Search and Filter
search_query = st.text_input("Search by Node Name or IP", "")
if search_query:
    df = df[df.apply(lambda row: search_query.lower() in row.astype(str).str.lower().values, axis=1)]

st.dataframe(df, use_container_width=True, hide_index=True)

st.sidebar.info("Update the Google Sheet to see changes here instantly.")
