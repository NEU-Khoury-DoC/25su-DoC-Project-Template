
import logging
logger = logging.getLogger(__name__)

import streamlit as st
from modules.nav import SideBarLinks
import plotly.express as px
import pandas as pd
import numpy as np
SideBarLinks()

import streamlit as st
import requests

st.title("📬 Find Your MEP Match")
st.markdown("Answer a few questions to get MEP recommendations aligned with your values.")





# ---------- Helper to load image from mepID ----------
def render_mep_image_from_id(mep_id, fallback_caption="No photo available"):
    if mep_id:
        photo_url = f"https://www.europarl.europa.eu/mepphoto/{mep_id}.jpg"
        st.image(photo_url, width=100)
    else:
        st.image(
            "https://upload.wikimedia.org/wikipedia/commons/thumb/e/ec/Unknown_person.jpg/240px-Unknown_person.jpg",
            width=100,
            caption=fallback_caption
        )

# ---------- EU Countries & Party Groups ----------
EU_COUNTRIES = [
    "Austria","Belgium","Bulgaria","Croatia","Cyprus","Czechia","Denmark","Estonia",
    "Finland","France","Germany","Greece","Hungary","Ireland","Italy","Latvia",
    "Lithuania","Luxembourg","Malta","Netherlands","Poland","Portugal","Romania",
    "Slovakia","Slovenia","Spain","Sweden"
]

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
    with st.form("recommender_form"):
        st.subheader("🎯 Match Calculator")
        percent_agree_current = st.slider("Agreement with your *current* party:", 0.0, 1.0, 0.7)
        percent_attendance = st.slider("Importance of attendance:", 0.0, 1.0, 0.85)
        my_party = st.selectbox("Your current party", PARTY_GROUPS)
        my_party_percentage = st.slider("Agreement with your *own* party:", 0.0, 1.0, 0.75)
        candidate_party = st.selectbox("Preferred MEP party group", PARTY_GROUPS)
        candidate_country = st.selectbox("Preferred MEP country", EU_COUNTRIES)
        submitted = st.form_submit_button("🔍 Find Matches")

# ---------- MEP Match Results ----------
if submitted:
    with right_col:
        with st.spinner("Finding your matches..."):
            response = requests.post("http://api:4000/r/generate", json={
                "percent_agree_current": percent_agree_current,
                "percent_attendance": percent_attendance,
                "my_party": my_party,
                "my_party_percentage": my_party_percentage,
                "candidate_party": candidate_party,
                "candidate_country": candidate_country
            })

        if response.status_code == 200:
            matches = response.json().get("recommendations", [])
            if matches:
                st.success("🍏 Here are your top MEP matches:")
                for match in matches[:3]:  # top 3 matches
                    full_name = f"{match['First Name']} {match['Last Name']}"
                    st.markdown(f"### 👤 {full_name}")
                    cols = st.columns([1, 3])
                    with cols[0]:
                        mep_id = match.get("MEP ID")
                        render_mep_image_from_id(mep_id, fallback_caption=full_name)
                    with cols[1]:
                        st.markdown(f"""
                        - **Country**: {match['Country']}  
                        - **Current Party**: {match['Current Party']}  
                        - **Party Alignment**: {round(match['Current Party Alignment Rate'] * 100)}%  
                        - **Attendance**: {round(match['Attendance Rate'] * 100)}%  
                        - **🧠 Match Score**: **{round(match['Cosine Score'] * 100)}%**
                        """)
                    st.markdown("---")
            else:
                st.warning("No MEPs matched your criteria. Try changing your filters.")
        else:
            st.error(f"Error {response.status_code}: {response.text}")
            
