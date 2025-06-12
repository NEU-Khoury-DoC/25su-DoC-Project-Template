import logging
logger = logging.getLogger(__name__)
import streamlit as st
from streamlit_extras.app_logo import add_logo
import pandas as pd
import pydeck as pdk
from urllib.error import URLError
from modules.nav import SideBarLinks
import plotly.express as px
from pages.styling_pages import traveler_font, traveler_font_country
import requests

SideBarLinks()

# add the logo
add_logo("assets/logo.png", height=400)

# set up the page
traveler_font("Top Tourism Attractions", False)
st.markdown(f"""
<div style="text-align: center; margin: 20px 0;">
    <img src="https://st4.depositphotos.com/5392356/39424/i/450/depositphotos_394249644-stock-photo-happy-traveling-tourists-friends-sightseeing.jpg"
         style="width: 800px; height: 400px; 
                border-radius: 8px; object-fit: cover;"
         alt="Tourism">
</div>
""", unsafe_allow_html=True)

countries_list = requests.get("http://web-api:4000/tourism/countrieslist").json()
for i in range(len(countries_list)):
    countries_list[i] = countries_list[i]["Country"]

countries_list = ["Select"] + countries_list
selected_country = st.selectbox("Select Country", countries_list)

if selected_country != "Select":
    traveler_font_country(selected_country)
    attractions_list = requests.get(f"http://web-api:4000/tourism/tourismattractions/{selected_country}").json()
    
    for i, attraction in enumerate(attractions_list, 1):
        with st.expander(f"{attraction['AttractionName']}"):
            col1, col2 = st.columns([1, 3])
            with col1:
                st.metric("Location", attraction['City'])
            with col2:
                if attraction['AttractionWebsite']:
                    st.markdown(f"🌐 **Website:** [{attraction['AttractionWebsite']}]({attraction['AttractionWebsite']})")
                else:
                    st.info("No website available")
