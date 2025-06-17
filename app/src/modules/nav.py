# Idea borrowed from https://github.com/fsmosca/sample-streamlit-authenticator

# This file has function to add certain functionality to the left side bar of the app

import streamlit as st


#### ------------------------ General ------------------------
def HomeNav():
    st.sidebar.page_link("Home.py", label="Home", icon="🏠")


def AboutPageNav():
    st.sidebar.page_link("pages/30_About.py", label="About", icon="🧠")


#### ------------------------ Examples for Role of party_leader ------------------------
def PartyLeaderHomeNav():
    st.sidebar.page_link(
        "pages/00_Party_Leader_Home.py", label="Party Leader Home", icon="👤"
    )


def PartyRecommenderNav():
    st.sidebar.page_link(
        "pages/01_Party_Recommend.py", label="Party Recruitment Dashboard", icon="🧲"
    )


def PartyCohesionNav():
    st.sidebar.page_link("pages/02_Cohesion_Monitor.py", label="Percent Dissent Predictor", icon="📈")

def MEPWatchlistNav():
    st.sidebar.page_link("pages/03_MEP_Watchlist.py", label="MEP Watchlist", icon="🔍")


## ------------------------ Examples for Role of political_journalist ------------------------
def PoliticalJournalistHomeNav():
    st.sidebar.page_link("pages/10_Political_Journalist_Home.py", label="Political Journalist Home", icon="👤")


def CohesionMonitorNav():
    st.sidebar.page_link(
        "pages/12_Party_Cohesion_Monitor.py", label="Dissent Overtime", icon="🖥️"
)

def MEPComparisonNav():
    st.sidebar.page_link("pages/13_MEP_Comparison.py", label="MEP Comparison", icon="🆚")

#### ------------------------ citizen Role ------------------------
def CitizenHomeNav():
    st.sidebar.page_link("pages/20_Citizen_Home.py", label="Citizen", icon="🖥️")

def MEPInfoNav():
    st.sidebar.page_link("pages/21_MEP_Party_Info.py", label="MEP & Party Info", icon="🏢")


def MEPMatchNav():
    st.sidebar.page_link("pages/22_Country_Match.py", label="Country Matcher", icon="🌍")



# --------------------------------Links Function -----------------------------------------------
def SideBarLinks(show_home=False):
    """
    This function handles adding links to the sidebar of the app based upon the logged-in user's role, which was put in the streamlit session_state object when logging in.
    """

    # add a logo to the sidebar always
    st.sidebar.image("assets/our_logo.png", width=280)

    # If there is no logged in user, redirect to the Home (Landing) page
    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False
        st.switch_page("Home.py")

    if show_home:
        # Show the Home page link (the landing page)
        HomeNav()

    # Show the other page navigators depending on the users' role.
    if st.session_state["authenticated"]:

        # Show World Bank Link and Map Demo Link if the user is a political strategy advisor role.
        if st.session_state["role"] == "party_leader":
            PartyLeaderHomeNav()
            PartyRecommenderNav()
            PartyCohesionNav()
            MEPWatchlistNav()

        # If the user role is usaid worker, show the Api Testing page
        if st.session_state["role"] == "political_journalist":
            PoliticalJournalistHomeNav()
            CohesionMonitorNav()
            MEPComparisonNav()

        # If the user is an administrator, give them access to the administrator pages
        if st.session_state["role"] == "citizen":
            CitizenHomeNav()
            MEPInfoNav()
            MEPMatchNav()

    # Always show the About page at the bottom of the list of links
    AboutPageNav()

    if st.session_state["authenticated"]:
        # Always show a logout button if there is a logged in user
        if st.sidebar.button("Logout"):
            del st.session_state["role"]
            del st.session_state["authenticated"]
            st.switch_page("Home.py")
