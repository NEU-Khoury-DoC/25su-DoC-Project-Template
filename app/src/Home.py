import logging
logger = logging.getLogger(__name__)

import streamlit as st
from PIL import Image
import requests

from modules.nav import SideBarLinks

# Set layout to wide
st.set_page_config(layout="wide")

# --- Add CSS for blue buttons ---
st.markdown("""
    <style>
    html, body, [class*="css"] {
        font-family: 'sans-serif' !important;
        background-color: #f0f4fb;
    }
    .block-container {
        padding: 3rem 5rem;
    }
    .stButton {
        padding-top: 28px;  /* Adjust as needed */
    }
    .stButton>button {
        background-color: #365fc7;
        color: white;
        padding: 0.3em 1.5em;
        border-radius: 8px;
        font-size: 16px;
        width: 100%;
    }
    div.stButton > button:hover {
        background-color: #264d99;
        color: white;
    }
    </style>
""", unsafe_allow_html=True)
from modules.nav import SideBarLinks


@st.cache_data
def get_all_party_leaders():

    response = requests.get("http://web-api:4000/u/users/role/1")
    if response.status_code != 200:
        st.error("Failed to access users")
        st.stop()


    users = response.json()

    return users



@st.cache_data
def get_all_political_journalists():
    response = requests.get("http://web-api:4000/u/users/role/2")
    if response.status_code != 200:
        st.error("Failed to access users")
        st.stop()


    users = response.json()

    return users


@st.cache_data
def get_all_citizens():
    response = requests.get("http://web-api:4000/u/users/role/3")
    if response.status_code != 200:
        st.error("Failed to access users")
        st.stop()


    users = response.json()

    return users

SideBarLinks()


pls = get_all_party_leaders()
pjs = get_all_political_journalists()
czs = get_all_citizens()

# Hero Section Layout
left, right = st.columns([2, 1], gap="large")

with left:
    st.markdown("## **Welcome to Loyalty Lines**")
    st.markdown("*Track EU votes. Understand MEP loyalty.*")
    
    rows = st.columns([2, 1]) 
    
    with rows[0]:
        pl_option = st.selectbox(
            "Log in as a Party Leader",
            [pl['firstName'] + " " + pl['lastName'] for pl in pls],
            key = 0,
        )
        
        pj_option = st.selectbox(
            "Log in as a Political Journalist",
            [pj['firstName'] + " " + pj['lastName'] for pj in pjs],
            key = 1,
        )
        
        cz_option = st.selectbox(
            "Log in as a Citizen",
            [cz['firstName'] + " " + cz['lastName'] for cz in czs],
            key = 2,
        )


    with rows[1]:
        if st.button("Log in", key=90, use_container_width=True):
            st.session_state['authenticated'] = True
            st.session_state['role'] = 'party_leader'
            st.session_state['name'] = pl_option
            st.switch_page("pages/00_Party_Leader_Home.py")

        if st.button("Log in", key=91, use_container_width=True):
            st.session_state['authenticated'] = True
            st.session_state['role'] = 'political_journalist'
            st.session_state['name'] = pl_option
            st.switch_page("pages/10_Political_Journalist_Home.py")

        if st.button("Log in", key=92, use_container_width=True):
            st.session_state['authenticated'] = True
            st.session_state['role'] = 'citizen'
            st.session_state['name'] = cz_option
            st.switch_page("pages/20_Citizen_Home.py")

with right:
    st.image("assets/blogo.png", width=400)