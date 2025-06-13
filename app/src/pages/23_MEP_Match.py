import logging
logger = logging.getLogger(__name__)

import streamlit as st
from modules.nav import SideBarLinks
import plotly.express as px
import pandas as pd
import numpy as np
import requests

SideBarLinks()

st.title("📬 Find Your MEP Match")
st.markdown("Use the sliders to tell us what matters most to you — party agreement or attendance — and discover which EU countries best reflect your values.")

# ---------- EU Party Groups ----------
PARTY_GROUPS = [
    "European People's Party",
    "Progressive Alliance of Socialists and Democrats",
    "Renew Europe",
    "Greens/European Free Alliance",
    "The Left (GUE/NGL)",
    "European Conservatives and Reformists",
    "Identity and Democracy",
    "Non-Inscrits"
]

# ---------- UI Layout ----------
left_col, right_col = st.columns([1, 2])

with left_col:
    st.subheader("🎯 Match Preferences")
    selected_party = st.selectbox("Which party are you recruiting for?", PARTY_GROUPS)
    agree_weight = st.slider("How important is party agreement?", 0.0, 1.0, 0.5)
    attendance_weight = st.slider("How important is attendance?", 0.0, 1.0, 0.5)
    submit = st.button("🔍 Show Heatmap")

# ---------- Map Generation ----------
if submit:
    with right_col:
        st.subheader("🗺️ EU Insight Map: Countries That Match Your Priorities")

        try:
            # Call your custom API endpoint (make sure to update the host/port as needed)
            response = requests.get("http://web-api:4000/b/get-country-heatmap", params={
                "agree": agree_weight * 100,
                "attendance": attendance_weight * 100,
                "party": selected_party
            })

            if response.status_code == 200:
                data = response.json()
                country_scores = pd.DataFrame(data)

                fig = px.choropleth(
                    country_scores,
                    locations="iso_alpha",
                    color="match_score",
                    hover_name="country",
                    hover_data={"country": True, "avg_dissent_rate": True, "match_score": True},
                    color_continuous_scale="Viridis",
                    range_color=(50, 100),
                    scope="europe",
                    title=f"🌍 Match Score by Country for {selected_party}"
                )

                st.plotly_chart(fig, use_container_width=True)
                st.caption("This map highlights the countries where MEPs best reflect your emphasis on party agreement and attendance.")

            else:
                st.error(f"API Error: {response.status_code} - {response.text}")

        except Exception as e:
            st.error(f"Failed to load data from the API: {str(e)}")