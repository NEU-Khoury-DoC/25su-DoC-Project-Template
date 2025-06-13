import streamlit as st
import pandas as pd
import requests


from modules.nav import SideBarLinks
SideBarLinks()

st.title("Find Your Top 10 MEP Matches")

# User-friendly input fields
agree = st.slider("How much should they currently agree with their own party?", 0, 100, 70)
attendance = st.slider("How often should they show up to vote?", 0, 100, 80)
party = st.selectbox("Which party are you recruiting for?", [
    'European People’s Party',
    'Renew Europe',
    'Progressive Alliance of Socialists and Democrats',
    'European Conservatives and Reformists',
    'Non-attached Members',
    'Europe of Sovereign Nations',
    'The Left in the European Parliament – GUE/NGL',
    'Greens/European Free Alliance',
    'Patriots for Europe',
    'Identity and Democracy'
])
party_pct = st.slider("How closely should they align with your party?", 0, 100, 80)
country = st.selectbox("What country are they from?", [
    'France', 'Germany', 'Italy', 'Belgium', 'Spain', 'Sweden', 'Netherlands'
])
country_weight = st.slider("How important is country match?", 0, 100, 10)

# Call API when button is clicked

if st.button("Get Fixed Recommendations"):
    try:
        url = "http://web-api:4000/b/recommender?agree=70&attendance=80&party=Patriots%20for%20Europe&party_pct=80&country=France&country_weight=10"
        response = requests.get(url)
        # response.raise_for_status()  # ← this only runs if response is defined

        data = response.json()
        # Always wrap in a list if it's a single dict
        if isinstance(data, dict):
            df = pd.DataFrame([data])
        else:
            df = pd.DataFrame(data)
        st.success("Results loaded successfully!")
        st.subheader("Top 10 Matching MEPs")
        st.dataframe(df)
    
    except requests.exceptions.RequestException as e:
        st.error(f"Request failed: {e}")
