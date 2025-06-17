import logging
logger = logging.getLogger(__name__)

import streamlit as st
from modules.nav import SideBarLinks

# Show appropriate sidebar links for the role of the currently logged in user
SideBarLinks()

st.title(f"Welcome Party Leader, {st.session_state['name']}.")
st.write('')
st.write('')
st.write('### What would you like to do today?')

if st.button('Party Recruitment Dashboard', 
             type='primary',
             use_container_width=True):
  st.switch_page('pages/01_Party_Recommend.py')

if st.button('Party Cohesion Monitor', 
             type='primary',
             use_container_width=True):
  st.switch_page('pages/02_Cohesion_Monitor.py')

if st.button('MEP Watchlist', 
             type='primary',
             use_container_width=True):
  st.switch_page('pages/03_MEP_Watchlist.py')

