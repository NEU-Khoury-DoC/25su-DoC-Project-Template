import streamlit as st
from streamlit_extras.app_logo import add_logo
from modules.nav import SideBarLinks

SideBarLinks()


st.write("# About Loyalty Lines")


st.markdown(
    """
        In an age of political contention, having transparent and accessible political data is essential to hold Members of the European Parliament accountable regarding their voting actions. Our application aims to visualize MEP party loyalty, identify frequent dissenters, and provide recommendations for party changes and civilian votes.

        Due to the high volume of votes that Parliament holds, it can be difficult for both party leaders and members to keep track of cohesion within the group. Currently, there is no interactive system that visualizes and predicts MEP voting patterns and party loyalties.

        Our application will provide an interface to view how cohesive a given political party is based on the percentage of MEPs within the party that vote together. It will visualize the hemicycle through the lens of party loyalty and also provide information for the MEPs themselves, specifically by computing a loyalty score for each. This will allow the application to predict future party changes, offer potential recommendations for party changes, and corroborate rhetoric with actual votes. It can also inform citizens how closely their MEP is in alignment with their party’s values so they can make an informed decision on whether to vote for that person again.

        With our app, we hope to streamline MEP data by providing clear insights for our user personas. By creating interactive visualizations, predictions, and loyalty scores, we hope to increase transparency and civic engagement across the EU.    
    """
)

# Add a button to return to home page
if st.button("Return to Home", type="primary"):
    st.switch_page("Home.py")
