import logging
logger = logging.getLogger(__name__)

import streamlit as st
from modules.nav import SideBarLinks

st.set_page_config(layout = 'wide')

# Show appropriate sidebar links for the role of the currently logged in user
SideBarLinks()

st.title(f"Welcome Citizen, {st.session_state['name']}.")
st.write('')
st.write('')
st.write('### What would you like to do today?')

if st.button('MEP & Political Party Information', 
             type='primary',
             use_container_width=True):
  st.switch_page('pages/21_MEP_Party_Info.py')

if st.button('Country Explorer', 
             type='primary',
             use_container_width=True):
  st.switch_page('pages/23_MEP_Match.py')
