import logging
logger = logging.getLogger(__name__)

import streamlit as st
from modules.nav import SideBarLinks
from pages.styling_pages import style_buttons, traveler_font, collage_form

st.set_page_config(layout = 'wide')

# Show appropriate sidebar links for the role of the currently logged in user

SideBarLinks()
style_buttons()
traveler_font(st.session_state['first_name'], True)
collage_form('https://images.unsplash.com/photo-1467269204594-9661b134dd2b?w=600',
             'https://www.insightvacations.com/wp-content/uploads/2024/01/caleb-miller-0Bs3et8FYyg-unsplash.jpg', 
             'https://cms.inspirato.com/ImageGen.ashx?image=%2Fmedia%2F5682444%2FLondon_Dest_16531610X.jpg&width=1081.5', 
             'https://www.planetware.com/wpimages/2020/02/france-in-pictures-beautiful-places-to-photograph-eiffel-tower.jpg', 
             'https://media.cnn.com/api/v1/images/stellar/prod/130928072317-01-copenhagen-restricted.jpg?q=w_4503,h_3001,x_0,y_0,c_fill',
             'Belgium',
             'Italy',
             'United Kingdom',
             'France',
             'Denmark')
st.write('')
traveler_font("What would you like to do today?", False)
if st.button('Where to Travel?', 
             type='primary',
             use_container_width=True):
  st.switch_page('pages/01_Where_To_Travel.py')


if st.button('Find Tourist Attractions', 
             type='primary',
             use_container_width=True):
  st.switch_page('pages/02_TouristAttractions.py')
