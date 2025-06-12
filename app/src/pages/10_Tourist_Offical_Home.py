import logging
logger = logging.getLogger(__name__)

import streamlit as st
from modules.nav import SideBarLinks
from pages.styling_pages import style_buttons, collage_form, offical_font

st.set_page_config(layout = 'wide')

# Show appropriate sidebar links for the role of the currently logged in user
SideBarLinks()
style_buttons()
offical_font(st.session_state['first_name'], True)
st.write('')
collage_form('https://www.cmswire.com/-/media/a7be4403acee498ca21e6861871358b3.ashx',
             'https://www.garageeks.com/wp-content/uploads/Screenshot-2023-10-10-alle-17.49.36.png',
             'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRwEWb3d3A0oNWEEEeI2MD1v7BGrmvQg4wM1Q&s',
             'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRn-5bqRP0Stp0UvcXPiN8Q2vJCNH2d_oyPAA&s',
             'https://www.torontosom.ca/wp-content/uploads/2022/04/the-difference-between-international-and-domestic-tourism.jpg',
             'Predict Future Tourism Numbers',
             'View Tourism Infrastructure Analytics',
             'Download Filtered Country Data',
             'Understand Factors that Impact Tourism',
             'Gain a Greater Insight to Tourism')

offical_font("What would you like to do today?", False)
if st.button('Predict Number of Tourists in Future Years', 
             type='primary',
             use_container_width=True):
  st.switch_page('pages/11_Tourism_Prediction.py')

if st.button('View Tourism Analytics', 
             type='primary',
             use_container_width=True):
  st.switch_page('pages/12_Tourism_Analytics.py')

  