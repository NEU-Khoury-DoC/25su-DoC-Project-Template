##################################################
# This is the main/entry-point file for the 
# sample application for your project
##################################################

# Set up basic logging infrastructure
import logging
logging.basicConfig(format='%(filename)s:%(lineno)s:%(levelname)s -- %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# import the main streamlit library as well
# as SideBarLinks function from src/modules folder
import streamlit as st
from modules.nav import SideBarLinks
from pages.styling_pages import style_buttons, style_front_image

# streamlit supports reguarl and wide layout (how the controls
# are organized/displayed on the screen).
st.set_page_config(layout = 'wide')

# If a user is at this page, we assume they are not 
# authenticated.  So we change the 'authenticated' value
# in the streamlit session_state to false. 
st.session_state['authenticated'] = False

# Use the SideBarLinks function from src/modules/nav.py to control
# the links displayed on the left-side panel. 
# IMPORTANT: ensure src/.streamlit/config.toml sets
# showSidebarNavigation = false in the [client] section
SideBarLinks(show_home=True)

# ***************************************************
#    The major content of this page
# ***************************************************

# set the title of the page and provide a simple prompt. 
style_buttons() 
style_front_image()

logger.info("Loading the Home page of the app")
st.write('\n\n')
st.write('\n')
st.write('#### Welcome. Who is logging in today?')

# For each of the user personas for which we are implementing
# functionality, we put a button on the screen that the user 
# can click to MIMIC logging in as that mock user. 

left_col, middle_col, right_col = st.columns(3)

with left_col:
    st.image("assets/traveler.jpg", use_container_width=True)
    if st.button("Act as Jacques Bon-voyage, a European Traveler", 
                 type='primary', 
                 use_container_width=True):
        # when user clicks the button, they are now considered authenticated
        st.session_state['authenticated'] = True
        # we set the role of the current user
        st.session_state['role'] = 'traveler'
        # we add the first name of the user (so it can be displayed on 
        # subsequent pages). 
        st.session_state['first_name'] = 'Jacques'
        # finally, we ask streamlit to switch to another page, in this case, the 
        # landing page for this particular user type
        logger.info("Logging in as Traveler Persona")
        st.switch_page('pages/00_Traveler_Home.py')

with middle_col:
    st.image("assets/official.jpg", use_container_width=True)
    if st.button("Act as Nina Petek, a National Director of Tourism", 
                 type='primary', 
                 use_container_width=True):
        st.session_state['authenticated'] = True
        st.session_state['role'] = 'tourist_offical'
        st.session_state['first_name'] = 'Nina'
        st.switch_page('pages/10_Tourist_Offical_Home.py')

with right_col:
    st.image("assets/researcher.jpg", use_container_width=True)
    if st.button("Act as Ellie Willems, a European Tourism Researcher", 
                 type='primary', 
                 use_container_width=True):
        st.session_state['authenticated'] = True
        st.session_state['role'] = 'reseacher'
        st.session_state['first_name'] = 'Ellie'
        st.session_state["AuthorID"] = 1
        st.switch_page('pages/20_Reseacher_Home.py')




