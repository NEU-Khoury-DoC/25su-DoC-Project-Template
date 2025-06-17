import logging
logger = logging.getLogger(__name__)

import streamlit as st
from modules.nav import SideBarLinks

st.set_page_config(layout = 'wide')

# Show appropriate sidebar links for the role of the currently logged in user
SideBarLinks()


st.title(f"Welcome Political Journalist, {st.session_state['name']}.")
st.write('')
st.write('')
st.write('### What would you like to do today?')

if st.button('Party Cohesion Monitor', 
             type='primary',
             use_container_width=True):
  st.switch_page('pages/12_Party_Cohesion_Monitor.py')


if st.button('MEP Comparison', 
             type='primary',
             use_container_width=True):
  st.switch_page('pages/13_MEP_Comparison.py')
