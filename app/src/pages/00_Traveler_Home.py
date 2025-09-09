import logging
logger = logging.getLogger(__name__)

import streamlit as st
from modules.nav import SideBarLinks

st.set_page_config(layout = 'wide')

# Show appropriate sidebar links for the role of the currently logged in user
SideBarLinks()

st.title(f"Welcome Traveler, {st.session_state['first_name']}.")
st.write('')
st.write('')
st.write('### What would you like to do today?')

if st.button('Where to Travel?', 
             type='primary',
             use_container_width=True):
  st.switch_page('pages/01_Where_To_Travel.py')

if st.button('Traffic Prediction', 
             type='primary',
             use_container_width=True):
  st.switch_page('pages/02_Traffic_Prediction.py')