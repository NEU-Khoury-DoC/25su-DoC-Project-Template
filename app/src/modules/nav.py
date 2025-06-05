# Idea borrowed from https://github.com/fsmosca/sample-streamlit-authenticator

# This file has function to add certain functionality to the left side bar of the app

import streamlit as st


#### ------------------------ General ------------------------
def HomeNav():
    st.sidebar.page_link("Home.py", label="Home", icon="🏠")


def AboutPageNav():
    st.sidebar.page_link("pages/30_About.py", label="About", icon="🧠")


#### ------------------------ Examples for Role of student ------------------------
def StudentHomeNav():
    st.sidebar.page_link(
        "pages/00_University_Student_Home.py", label="University Student Home", icon="👩‍🎓"
    )


def StudentMapNav():
    st.sidebar.page_link(
        "pages/01_Student_Map.py", label="Country Recommendation Map", icon="🗺️"
    )


def UniversityNav():
    st.sidebar.page_link("pages/04_University_Recs.py", label="University Recommendations", icon="🏫")


## ------------------------ Examples for Role of policymaker ------------------------
def PolicymakerNav():
    st.sidebar.page_link("pages/10_Policymaker_Home.py", label="Policymaker Home", icon="👨‍💼")


def PolicyNav():
    st.sidebar.page_link(
        "pages/11_Policy_Implementation.py", label="Policy Implementation", icon="📰"
    )


def SimilarityNav():
    st.sidebar.page_link(
        "pages/12_Similar_Countries.py", label="Similar Countries", icon="🗺️"
    )

#### ------------------------ Activist Role ------------------------
def ActivistHomeNav():
    st.sidebar.page_link("pages/20_Activist_Home.py", label="Activist Home", icon="👩‍💼")

def ExpansionNav():
    st.sidebar.page_link("pages/21_Expansion_Map.py", label="Expansion Map", icon="🗺️")

def QoLChangeNav():
    st.sidebar.page_link("pages/22_QoL_Change.py", label="QoL Change", icon="📈")

def CurrentOrgsNav():
    st.sidebar.page_link("pages/23_Current_Orgs.py", label="Current Organizations", icon="🏢")

# --------------------------------Links Function -----------------------------------------------
def SideBarLinks(show_home=False):
    """
    This function handles adding links to the sidebar of the app based upon the logged-in user's role, which was put in the streamlit session_state object when logging in.
    """

    # add a logo to the sidebar always
    st.sidebar.image("assets/logo.png", width=150)

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
        if st.session_state["role"] == "student":
            StudentHomeNav()
            StudentMapNav()
            UniversityNav()

        # If the user role is usaid worker, show the Api Testing page
        if st.session_state["role"] == "policymaker":
            PolicymakerNav()
            PolicyNav()
            SimilarityNav()

        # If the user is an administrator, give them access to the administrator pages
        if st.session_state["role"] == "activist":
            ActivistHomeNav()
            ExpansionNav()
            QoLChangeNav()
            CurrentOrgsNav()


    # Always show the About page at the bottom of the list of links
    AboutPageNav()

    if st.session_state["authenticated"]:
        # Always show a logout button if there is a logged in user
        if st.sidebar.button("Logout"):
            del st.session_state["role"]
            del st.session_state["authenticated"]
            st.switch_page("Home.py")
