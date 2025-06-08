import logging
logger = logging.getLogger(__name__)

import streamlit as st
from modules.nav import SideBarLinks
from pages.styling_pages import style_buttons

st.set_page_config(layout = 'wide')

# Show appropriate sidebar links for the role of the currently logged in user

SideBarLinks()
style_buttons()

st.title(f"Welcome Traveler, {st.session_state['first_name']}.")
st.markdown("""
<style>
.welcome-collage {
    display: grid;
    grid-template-columns: 2fr 1fr 1fr;
    grid-template-rows: 200px 200px;
    gap: 10px;
    border-radius: 15px;
    overflow: hidden;
    margin: 2rem 0;
    box-shadow: 0 10px 30px rgba(0,0,0,0.1);
}

.collage-item {
    background-size: cover;
    background-position: center;
    position: relative;
    transition: transform 0.3s ease;
}

.collage-item:hover {
    transform: scale(1.05);
    z-index: 2;
}

.collage-main {
    grid-row: 1 / 3;
    background-image: url('https://images.unsplash.com/photo-1467269204594-9661b134dd2b?w=600');
}

.collage-top-right {
    background-image: url('https://www.insightvacations.com/wp-content/uploads/2024/01/caleb-miller-0Bs3et8FYyg-unsplash.jpg');
}

.collage-bottom-right {
    background-image: url('https://cms.inspirato.com/ImageGen.ashx?image=%2Fmedia%2F5682444%2FLondon_Dest_16531610X.jpg&width=1081.5');
}
            
.collage-bottom {
    background-image: url('https://www.planetware.com/wpimages/2020/02/france-in-pictures-beautiful-places-to-photograph-eiffel-tower.jpg');
}
            
.collage-bottom-left {
    background-image: url('https://media.cnn.com/api/v1/images/stellar/prod/130928072317-01-copenhagen-restricted.jpg?q=w_4503,h_3001,x_0,y_0,c_fill');
}

.image-overlay {
    position: absolute;
    bottom: 0;
    left: 0;
    right: 0;
    background: linear-gradient(transparent, rgba(0,0,0,0.7));
    color: white;
    padding: 1rem;
    font-weight: 600;
}
</style>

<div class="welcome-collage">
    <div class="collage-item collage-main">
        <div class="image-overlay">Belgium</div>
    </div>
    <div class="collage-item collage-top-right">
        <div class="image-overlay">Italy</div>
    </div>
    <div class="collage-item collage-bottom-right">
        <div class="image-overlay">United Kingdom</div>
    </div>
    <div class="collage-item collage-bottom">
        <div class="image-overlay">France</div>
    </div>
    <div class="collage-item collage-bottom-left">
        <div class="image-overlay">Denmark</div>
    </div>
</div>
""", unsafe_allow_html=True)
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