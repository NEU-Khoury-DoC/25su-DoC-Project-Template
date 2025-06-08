import logging
logger = logging.getLogger(__name__)

import streamlit as st
from modules.nav import SideBarLinks
from pages.styling_pages import style_buttons
import requests


st.set_page_config(layout = 'wide')

SideBarLinks()
style_buttons()

st.success("🥳 Post Successful")
if st.button('View Existing Posts', 
             type='primary',
             use_container_width=True):
  st.switch_page('pages/22_Reseacher_View.py')