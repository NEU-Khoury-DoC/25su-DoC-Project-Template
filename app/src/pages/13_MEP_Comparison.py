import logging
logger = logging.getLogger(__name__)
import streamlit as st
from modules.nav import SideBarLinks
import requests
import pandas as pd
import plotly.express as px

st.set_page_config(layout = 'wide') 

SideBarLinks()

@st.cache_data
def get_meps():
    # ----------------------------
    # Build DataFrame with party info
    # ----------------------------
    resp = requests.get("http://web-api:4000/m/meps")
    meps = resp.json() if resp.status_code == 200 else []


    mep_df = pd.DataFrame()
    for mep in meps:
        try:
            party_resp = requests.get(f'http://web-api:4000/m/meps/{mep["mepID"]}/party')
            party = party_resp.json().get("partyName", "Unknown")
        except:
            party = "Unknown"

        row = pd.DataFrame([{
            "mepID": mep["mepID"],
            "name": mep["name"],
            "party": party,
            "country": mep["countryOfOrigin"],
            "loyaltyScore": mep["loyaltyScore"],
            "photoURL": mep.get("photoURL"),
            "percentDisagree": mep["percentDisagree"],
            "percentTurnout": mep["percentTurnout"]
        }])
        mep_df = pd.concat([mep_df, row], ignore_index=True)

    return mep_df   

 

st.title("🤝 Compare Two MEPs")

# ----------------------------
# Load MEP data from API
# ----------------------------
mep_df = get_meps()

# ----------------------------
# MEP A & B Selectors
# ----------------------------
colA, colB = st.columns(2)

mep_names = mep_df["name"].tolist()

with colA:
    mepA_name = st.selectbox("Select MEP A", mep_names, key="mepA")

with colB:
    mepB_name = st.selectbox("Select MEP B", mep_names, key="mepB")

if mepA_name == mepB_name:
    st.warning("Please select two different MEPs for comparison.")
    st.stop()

mepA = mep_df[mep_df["name"] == mepA_name].iloc[0]
mepB = mep_df[mep_df["name"] == mepB_name].iloc[0]

# Side-by-Side Profile Display
col1, col2 = st.columns(2)

with col1:
    st.subheader(f"👤 {mepA['name']}")
    if mepA["photoURL"]:
        st.image(mepA["photoURL"], width=160)
    st.markdown(f"**Country**: {mepA['country']}")
    st.markdown(f"**Party**: {mepA['party']}")
    st.markdown(f"**Loyalty Score**: {mepA['loyaltyScore']}%")

with col2:
    st.subheader(f"👤 {mepB['name']}")
    if mepB["photoURL"]:
        st.image(mepB["photoURL"], width=160)
    st.markdown(f"**Country**: {mepB['country']}")
    st.markdown(f"**Party**: {mepB['party']}")
    st.markdown(f"**Loyalty Score**: {mepB['loyaltyScore']}%")



# Voting Breakdown Chart
st.markdown("### 📊 Voting Breakdown Comparison")

compare_df = pd.DataFrame({
    "Category": ["Agreed", "Dissented", "Did Vote"] * 2,
    "Percentage": [
        mepA["loyaltyScore"], mepA["percentDisagree"], mepA["percentTurnout"],
        mepB["loyaltyScore"], mepB["percentDisagree"], mepB["percentTurnout"],
    ],
    "MEP": [mepA["name"]] * 3 + [mepB["name"]] * 3
})

fig = px.bar(
    compare_df,
    x="Category",
    y="Percentage",
    color="MEP",
    barmode="group",
    title="Voting Record Comparison",
    labels={"Percentage": "% of Votes"}
)
fig.update_layout(yaxis_range=[0, 100])
st.plotly_chart(fig, use_container_width=True)