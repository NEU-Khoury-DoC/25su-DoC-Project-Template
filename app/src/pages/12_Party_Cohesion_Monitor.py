import streamlit as st
import requests
from streamlit_extras.app_logo import add_logo
from modules.nav import SideBarLinks
import plotly.express as px
import pandas as pd

SideBarLinks()

st.title("📈 Party Dissent Monitor")
st.markdown("### _Track how party loyalty has changed over time._")
st.markdown("This vizualization shows how the percent of dissenters has changed for each party as time has passed.")
st.markdown("Time is measured by week index, which refers to the week in which the vote occurred chronologically relative to other votes in the available data.")
st.markdown("The data in this graph is from 2021 - 2025. Week 1 is the least recent.")

st.markdown(" ")
st.markdown("_Click party names in the legend to add/remove them from the plot._")

resp = requests.get("http://web-api:4000/t/times")
time_resp = resp.json() if resp.status_code == 200 else []

# ----------------------------
# Build DataFrame with time info
# ----------------------------
time_df = pd.DataFrame([{
    "Week Index": int(row["adjusted_week"]),
    "Party": row["party"],
    "Percent Dissent": float(row["percent_dissent"])} for row in time_resp])


avg_df = time_df.groupby(["Week Index", "Party"], as_index=False)["Percent Dissent"].mean()

fig = px.line(
    avg_df,
    x="Week Index",
    y="Percent Dissent",
    color="Party",
    title="Average Party Dissent Per Week",
    labels={"Week Index": "Week", "Percent Dissent": "Average Percent Dissent"}
)

st.plotly_chart(fig, use_container_width=True)