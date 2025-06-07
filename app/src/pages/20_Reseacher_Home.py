import logging
logger = logging.getLogger(__name__)

import streamlit as st
from modules.nav import SideBarLinks
import requests
from pages.styling_pages import style_buttons

st.set_page_config(layout = 'wide')

SideBarLinks()
style_buttons()

st.title('Welcome Reseacher, Ellie')
st.markdown("""
<style>
.research-collage {
    display: grid;
    grid-template-columns: 2fr 1fr 1fr;
    grid-template-rows: 200px 200px;
    gap: 10px;
    border-radius: 15px;
    overflow: hidden;
    margin: 2rem 0;
    box-shadow: 0 10px 30px rgba(0,0,0,0.1);
}

.research-item {
    background-size: cover;
    background-position: center;
    background-repeat: no-repeat;
    position: relative;
    transition: transform 0.3s ease;
}

.research-item:hover {
    transform: scale(1.02);
    z-index: 2;
}

.research-main {
    grid-row: 1 / 3;
    grid-column: 1;
    background-image: url('https://www.usatoday.com/gcdn/-mm-/d2a691f1f64d8069f144791917ccdcf1e7d1fa16/c=0-0-1800-1015/local/-/media/USATODAY/test/2013/11/01/1383327500000-692-FreewaySlovenia.jpg?width=1800&height=1015&fit=crop&format=pjpg&auto=webp');
}

.research-top-right {
    grid-row: 1;
    grid-column: 2;
    background-image: url('https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRv501qROXIU_LqNNg6rIclHtTGf3sNuqltOw&s');
}

.research-bottom-right {
    grid-row: 2;
    grid-column: 2;
    background-image: url('https://compote.slate.com/images/49bf62d0-9a1f-4207-bd43-494c0ce31431.jpg?crop=568%2C379%2Cx0%2Cy0&width=2200');
}

.research-top-far-right {
    grid-row: 1;
    grid-column: 3;
    background-image: url('https://pxlv6-mdxacuk.terminalfour.net/fit-in/2200x1610/filters:quality(75)/64x0:1376x960/prod01/channel_4/media/middlesexmu/course-images/mba-short-learning-programme-application/businesswoman-pointing-at-flip-chart-and-discussi-2024-11-14-11-39-13-utc.jpg');
}

.research-bottom-far-right {
    grid-row: 2;
    grid-column: 3;
    background-image: url('https://images.unsplash.com/photo-1521587760476-6c12a4b040da?w=400');
}

.research-overlay {
    position: absolute;
    bottom: 0;
    left: 0;
    right: 0;
    background: linear-gradient(transparent, rgba(0,0,0,0.8));
    color: white;
    padding: 1rem;
    font-weight: 600;
    font-size: 14px;
}
</style>

<div class="research-collage">
    <div class="research-item research-main">
        <div class="research-overlay">View Road Statistics on the Country Level</div>
    </div>
    <div class="research-item research-top-right">
        <div class="research-overlay">Create Posts Regarding Your Findings</div>
    </div>
    <div class="research-item research-bottom-right">
        <div class="research-overlay">View Others Users Insights</div>
    </div>
    <div class="research-item research-top-far-right">
        <div class="research-overlay">Study Trends</div>
    </div>
    <div class="research-item research-bottom-far-right">
        <div class="research-overlay">Learn More About Europe</div>
    </div>
</div>
""", unsafe_allow_html=True)
st.write('')
st.write('### What would you like to do today?')
if st.button('Create Posts', 
             type='primary',
             use_container_width=True):
  st.switch_page('pages/21_Reseacher_Notes.py')

if st.button('View Existing Posts', 
             type='primary',
             use_container_width=True):
  st.switch_page('pages/22_Reseacher_View.py')


