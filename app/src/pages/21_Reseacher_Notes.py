import logging
import streamlit as st
import requests
import pandas as pd
from PIL import Image
import json
from modules.nav import SideBarLinks
from pages.styling_pages import style_buttons, researcher_font


logger = logging.getLogger(__name__)

st.set_page_config(layout='wide')
researcher_font("Research Post", False)
SideBarLinks()
style_buttons()

with st.form("research_form"):
    title = st.text_input("Input Title to Post Here")
    notes = st.text_area(
        "Input Notes Here",
        placeholder="Enter your research notes, thoughts, or queries here...",
        height=150,
        key="notes_input"
    )
    
    if notes:
        st.caption(f"Character count: {len(notes)}")
    
    st.divider()
    submitted = st.form_submit_button("📤 Submit Post", type="primary")
    
    if submitted:
        if title and notes:
            post_data = {
                "Title": title,
                "Research": notes,
                "AuthorID": st.session_state["AuthorID"]
            }
            
            try:
                response = requests.post(
                    "http://web-api:4000/researcher/posts",
                    json=post_data
                )

                if response.status_code == 201:
                    st.switch_page("pages/23_Success_Page.py")
                else:
                    st.error(f"Error: {response.json()['error']}")
                    
            except Exception as e:
                st.error(f"Connection error: {str(e)}")
        else:
            st.error("Please fill in Title and Notes!")