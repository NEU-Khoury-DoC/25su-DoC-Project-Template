# Idea borrowed from https://github.com/fsmosca/sample-streamlit-authenticator

# This file has function to add certain functionality to the left side bar of the app

import streamlit as st


#### ------------------------ General ------------------------
def HomeNav():
    st.sidebar.page_link("Home.py", label="Home", icon="🏠")


def AboutPageNav():
    st.sidebar.page_link("pages/30_About.py", label="About", icon="🧠")


#### ------------------------ Examples for Role of traveler ------------------------
def TravelerHomeNav():
    st.sidebar.page_link(
        "pages/00_Traveler_Home.py", label="Traveler Home", icon="🏠"
    )


def WhereToTravelNav():
    st.sidebar.page_link(
        "pages/01_Where_To_Travel.py", label="Where to travel?", icon="🚗"
    )


def MapDemoNav():
    st.sidebar.page_link("pages/02_TouristAttractions.py", label="Tourist Attractions", icon="🏰")


## ------------------------ Examples for Role of tourist_offical ------------------------
def OfficalHomeNav():
    st.sidebar.page_link(
        "pages/10_Tourist_Offical_Home.py", label="Offical Home", icon="🏠"
    )

def TourismAnalyticsNav():
    st.sidebar.page_link("pages/12_Tourism_Analytics.py", label="Tourism Analytics", icon="📊")


def PredictionNav():
    st.sidebar.page_link(
        "pages/11_Tourism_Prediction.py", label="Tourism Prediction", icon="📈"
    )


#### ------------------------ Examples for Role of reseacher ------------------------
def AdminPageNav():
    st.sidebar.page_link("pages/20_Reseacher_Home.py", label="Reseacher Home", icon="🏠")
    st.sidebar.page_link(
        "pages/21_Reseacher_Notes.py", label="Create Post", icon="📝"
    )
    st.sidebar.page_link(
        "pages/22_Reseacher_View.py", label="View Posts", icon="🔍"
    )


# --------------------------------Links Function -----------------------------------------------
def SideBarLinks(show_home=False):
    """
    This function handles adding links to the sidebar of the app based upon the logged-in user's role, which was put in the streamlit session_state object when logging in.
    """

    # add a logo to the sidebar always
    st.sidebar.image("assets/eurotour.png", width=400)

    # If there is no logged in user, redirect to the Home (Landing) page
    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False
        st.switch_page("Home.py")

    if show_home:
        # Show the Home page link (the landing page)
        HomeNav()

    # Show the other page navigators depending on the users' role.
    if st.session_state["authenticated"]:

        # Show the wher to travel Link and traffic prediction link if the user is a traveler role.
        if st.session_state["role"] == "Tourist":
            TravelerHomeNav()
            WhereToTravelNav()
            MapDemoNav()

        # If the user role is usaid worker, show the Api Testing page
        if st.session_state["role"] == "National Official":
            OfficalHomeNav()
            PredictionNav()
            TourismAnalyticsNav()

        # If the user is an administrator, give them access to the administrator pages
        if st.session_state["role"] == "Researcher":
            AdminPageNav()

    # Always show the About page at the bottom of the list of links
    AboutPageNav()

    if st.session_state["authenticated"]:
        # Always show a logout button if there is a logged in user
        if st.sidebar.button("Logout"):
            del st.session_state["role"]
            del st.session_state["authenticated"]
            st.switch_page("Home.py")
