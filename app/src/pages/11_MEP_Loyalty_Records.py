import streamlit as st
import requests
import pandas as pd
import plotly.express as px
from modules.nav import SideBarLinks


@st.cache_data
def get_mep_data():
    # Load MEPs
    response = requests.get("http://web-api:4000/m/meps")
    if response.status_code != 200:
        st.error("Failed to load MEPs.")
        st.stop()

    meps = response.json()

    # Build DataFrame with party info
    rows = []
    for mep in meps:
        party_resp = requests.get(f"http://web-api:4000/m/meps/{mep['mepID']}/party")
        party_name = party_resp.json().get("partyName", "Unknown") if party_resp.status_code == 200 else "Unknown"

        rows.append({
            "mepID": mep["mepID"],
            "name": mep["name"],
            "party": party_name,
            "country": mep["countryOfOrigin"],
            "loyaltyScore": mep["loyaltyScore"],
            "photoURL": mep.get("photoURL")
        })

    return pd.DataFrame(rows)





# Setup
SideBarLinks()
st.title("📄 MEP Party Loyalty Records")

st.markdown("Search and select a Member of European Parliament (MEP) to view their party alignment, origin, loyalty score, and voting breakdown.")

with st.spinner("Retrieving MEP information..."):
    mep_data = get_mep_data()

# MEP Selection
selected_name = st.selectbox("Select MEP", mep_data["name"])
selected = mep_data[mep_data["name"] == selected_name].iloc[0]

# Display Headshot & Details

col1, col2 = st.columns([1, 3])
with col1:
    if selected["photoURL"]:
        st.image(selected["photoURL"], width=160, caption=selected_name)
    else:
        st.write("No photo available.")

with col2:
    st.subheader(selected_name)
    st.markdown(f"**Party**: {selected['party']}")
    st.markdown(f"**Country**: {selected['country']}")
    st.markdown(f"**Overall Loyalty Score**: {selected['loyaltyScore']}%")

# Fetch Score Breakdown from API
score_resp = requests.get(f"http://web-api:4000/m/mep/{selected['mepID']}/score")
if score_resp.status_code == 200:
    score_data = score_resp.json()
    agreed = float(score_data.get("agreed", 0))
    dissented = float(score_data.get("dissented", 0))
    not_voted = float(score_data.get("notVoted", 0))






    
else:
    st.warning("Voting breakdown unavailable.")
    agreed, dissented, not_voted = 0, 0, 0

# Voting Breakdown Chart
st.markdown("### Voting Record Breakdown")

chart_df = pd.DataFrame({
    "Category": ["Agreed", "Dissented", "Did Not Vote"],
    "Percentage": [agreed, dissented, not_voted]
})

fig = px.bar(
    chart_df,
    x="Category",
    y="Percentage",
    color="Category",
    color_discrete_sequence=["#4CAF50", "#9449ba", "#9E9E9E"],
    labels={"Percentage": "% of Votes"},
)
fig.update_layout(yaxis_range=[0, 100], showlegend=False)
st.plotly_chart(fig)

# Footer
st.markdown("---")
st.caption("Explore party loyalty and voting behavior of MEPs across the European Parliament.")