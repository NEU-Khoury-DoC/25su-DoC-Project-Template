import logging
logger = logging.getLogger(__name__)

import streamlit as st
from modules.nav import SideBarLinks
import requests
from pages.styling_pages import style_buttons, researcher_font, collage_form

st.set_page_config(layout = 'wide')
SideBarLinks()
style_buttons()
researcher_font(st.session_state['first_name'], True)
collage_form('https://www.usatoday.com/gcdn/-mm-/d2a691f1f64d8069f144791917ccdcf1e7d1fa16/c=0-0-1800-1015/local/-/media/USATODAY/test/2013/11/01/1383327500000-692-FreewaySlovenia.jpg?width=1800&height=1015&fit=crop&format=pjpg&auto=webp',
             'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRv501qROXIU_LqNNg6rIclHtTGf3sNuqltOw&s',
             'https://compote.slate.com/images/49bf62d0-9a1f-4207-bd43-494c0ce31431.jpg?crop=568%2C379%2Cx0%2Cy0&width=2200',
             'https://media.istockphoto.com/id/1071915654/photo/excited-black-coach-make-flipchart-presentation-for-employees.jpg?s=612x612&w=0&k=20&c=1kxSV8DLbhJ2vee0ulwOSgVYU4v7HfrO-WMbAXIro-g=',
             'https://images.unsplash.com/photo-1521587760476-6c12a4b040da?w=400',
             'View Road Statistics on the Country Level',
             'Create Posts Regarding Your Findings',
             'View Others Users Insights',
             'Study Trends',
             'Learn More About Europe')
st.write('')
researcher_font("What would you like to do today?", False)

if st.button('Create Posts', 
             type='primary',
             use_container_width=True):
  st.switch_page('pages/21_Reseacher_Notes.py')

if st.button('View Existing Posts', 
             type='primary',
             use_container_width=True):
  st.switch_page('pages/22_Reseacher_View.py')


