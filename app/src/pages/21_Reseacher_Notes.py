import logging
import streamlit as st
import requests
import pandas as pd
from PIL import Image
import json
from modules.nav import SideBarLinks
from pages.styling_pages import style_buttons


logger = logging.getLogger(__name__)

st.set_page_config(layout='wide')
SideBarLinks()
style_buttons()

st.title("Research Post & Data Upload")

with st.form("research_form"):
    st.header("📝 Jot down thoughts and queries")
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
    submitted = st.form_submit_button("📤 Submit Research Post", type="primary")
    
    if submitted:
        if title and notes:
            post_data = {
                "Title": title,
                "Research": notes,
                "AuthorID": st.session_state["AuthorID"]
            }
            
            try:
                response = requests.post(
                    "http://web-api:4000/researcher/new_post",
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
st.divider()