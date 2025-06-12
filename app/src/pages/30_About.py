import streamlit as st
from streamlit_extras.app_logo import add_logo
from modules.nav import SideBarLinks

SideBarLinks()

st.write("# About the Authors ")
left_col, middle_col_one, middle_col_two, right_col = st.columns(4)

with left_col:
    st.image("assets/SeanPicture.PNG", use_container_width=True)
    st.markdown("**Sean Behan**")
    st.text("I am a rising second year studying computer science with a concentration in AI with a minor in usiness administration")

with middle_col_one:
    st.image("assets/aidanpic.jpeg", use_container_width=True)
    st.markdown("**Aidan Kelly**")

with middle_col_two:
    st.image("assets/SeanPicture.PNG", use_container_width=True)
    st.markdown("**Gabby Montalvo**")

with right_col:
    st.image("assets/SeanPicture.PNG", use_container_width=True)
    st.markdown("**Maria**")

st.write("# Problem EuroTour Addresses")
st.markdown(
    """
    Despite the vast amount of public data on tourism and road infrastructure within the E.U., 
    there is no unified platform that transforms this information into a meaningful guidance tool 
    for a diverse range of users. 
    - Casual road trippers often struggle to plan efficient/affordable 
    trips due to overly technical datasets on road quality, traffic, and travel costs. 
    - Meanwhile, national officials tasked with promoting tourism and improving infrastructure lack accessible 
    tools to benchmark their country’s performance, predict tourism trends, or assess the effectiveness 
    of public investment in transportation. 
    - Academic researchers face yet another barrier: while they 
    need historical and comparative data for modeling and publication, much of the available information 
    is fragmented or lacks interoperability.
    """
)

# Add a button to return to home page
if st.button("Return to Home", type="primary"):
    st.switch_page("Home.py")
