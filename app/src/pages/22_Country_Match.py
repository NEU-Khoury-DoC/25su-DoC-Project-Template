import streamlit as st
import plotly.express as px
import pandas as pd
import requests
from modules.nav import SideBarLinks

SideBarLinks()

st.title("📬 Find Your Country Match")
st.markdown("Select a party to see which EU countries have MEPs most loyal to it.")

# Party Selection
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

selected_party = st.selectbox("Which party are you most aligned with?", PARTY_GROUPS)
submit = st.button("🔍 Show Heatmap")

# Map
if submit:
    try:
        response = requests.get("http://web-api:4000/b/get-country-heatmap", params={
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
                hover_data={"avg_dissent_rate": True, "match_score": True},
                color_continuous_scale="Viridis",
                range_color=(0, 100),
                scope="europe",
                title=f"🌍 Loyalty to {selected_party} by Country"
            )

            st.plotly_chart(fig, use_container_width=True)
            st.caption("This map shows which EU countries have MEPs most loyal to the selected party.")

            st.subheader("📊 Loyalty Details")
            st.dataframe(country_scores.sort_values("match_score", ascending=False))

        else:
            st.error(f"API Error: {response.status_code} - {response.text}")

    except Exception as e:
        st.error(f"Failed to load data from the API: {str(e)}")
