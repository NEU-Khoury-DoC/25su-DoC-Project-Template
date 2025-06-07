import logging
logger = logging.getLogger(__name__)
import pandas as pd
import streamlit as st
from streamlit_extras.app_logo import add_logo
import world_bank_data as wb
import matplotlib.pyplot as plt
import numpy as np
import plotly.express as px
from modules.nav import SideBarLinks
from pages.styling_pages import style_buttons
import requests

# Call the SideBarLinks from the nav module in the modules directory
SideBarLinks()
style_buttons()

st.header('Lost on where to travel in Europe?')
st.subheader('No Worries! Input your preferences below!')

with st.form("traveler_form"):

    costSlider = st.slider("How important is saving money on fuel/travel cost?", 0, 10, 5)
    trafficSlider = st.slider("How much do you value avoiding long travel times/traffic?", 0, 10, 5)
    tourismSlider = st.slider("How important is it to visit high tourism areas?", 0, 10, 5)

    submitted = st.form_submit_button("📤 Submit Research Post", type="primary")

def empty_visual(): 
    fig = px.choropleth(locationmode='ISO-3', 
                    scope='europe', 
                    ) 
    fig.update_layout(
        margin = dict(l=10, r = 10, t = 35, b = 0), 
        width = 500, 
        height = 300, 
        title = (f"Top 5 Recommended Countries"), 
    )
    #fig.show() 
    return fig

def map_visual(country_dataframe):
    eu_iso_codes = {
    "Austria": "AUT",
    "Belgium": "BEL",
    "Bulgaria": "BGR",
    "Croatia": "HRV",
    "Cyprus": "CYP",
    "Czechia": "CZE",
    "Denmark": "DNK",
    "Estonia": "EST",
    "Finland": "FIN",
    "France": "FRA",
    "Germany": "DEU",
    "Greece": "GRC",
    "Hungary": "HUN",
    "Ireland": "IRL",
    "Italy": "ITA",
    "Latvia": "LVA",
    "Lithuania": "LTU",
    "Luxembourg": "LUX",
    "Malta": "MLT",
    "Netherlands": "NLD",
    "Poland": "POL",
    "Portugal": "PRT",
    "Romania": "ROU",
    "Slovakia": "SVK",
    "Slovenia": "SVN",
    "Spain": "ESP",
    "Sweden": "SWE"
}
    country_dataframe["ISO"] = country_dataframe["Country"].map(eu_iso_codes)
    country_dataframe["Match Rating"] = country_dataframe["Similarity"]

    fig = px.choropleth(country_dataframe, locations="ISO",
                    color="Match Rating", 
                    locationmode='ISO-3',
                    hover_name = "Country", 
                    scope='europe',         
                    color_continuous_scale=px.colors.sequential.Teal, 
                    ) 
    fig.update_layout(
        margin = dict(l=10, r = 10, t = 35, b = 0), 
        width = 500, 
        height = 300, 
        title = (f"Top 5 Recommended Countries"), 
    )
    #fig.show()       
    return fig 




if submitted:
    try:
        
        response = requests.get(
            f"http://web-api:4000/tourism/recommender/{costSlider}/{trafficSlider}/{tourismSlider}"
        )

        if response.status_code == 200:
            st.plotly_chart(map_visual(pd.DataFrame(response.json())))
            for i in range(len(response.json())):
                st.write(f"{i + 1}) {response.json()[i]['Country']}")
            
        else:
            st.error(f"Error: {response.json()['error']}")
            
    except Exception as e:
        st.error(f"Connection error: {str(e)}")

else:
    st.plotly_chart(empty_visual())