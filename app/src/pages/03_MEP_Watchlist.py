import streamlit as st
import requests
from modules.nav import SideBarLinks

# Sidebar nav
SideBarLinks()

# Constants
USER_ID = 1
WATCHLIST_URL = f"http://web-api:4000/w/user/{USER_ID}/watchlists"
ALL_MEPS_URL = "http://web-api:4000/w/all_meps"

# Fetch watchlist
def get_watchlist():
    try:
        res = requests.get(WATCHLIST_URL)
        if res.status_code == 200:
            return res.json()
        st.error(f"Watchlist error {res.status_code}: {res.text}")
    except Exception as e:
        st.error(f"Watchlist fetch failed: {e}")
    return []

# Fetch MEPs for dropdown
def get_all_meps():
    try:
        res = requests.get(ALL_MEPS_URL)
        if res.status_code == 200:
            return res.json()
        st.error(f"MEP list error {res.status_code}: {res.text}")
    except Exception as e:
        st.error(f"MEP list fetch failed: {e}")
    return []

# Add MEP
def add_to_watchlist(mep_id):
    try:
        res = requests.post(WATCHLIST_URL, json={"mepID": mep_id})
        if res.status_code == 201:
            st.success("✅ MEP added.")
            st.rerun()
        elif res.status_code == 409:
            st.warning("⚠️ MEP already in watchlist.")
        else:
            msg = res.json().get("error", "Something went wrong.")
            st.error(f"❌ Failed to add: {msg}")
    except Exception as e:
        st.error(f"Add failed: {e}")

# Remove MEP
def remove_from_watchlist(mep_id):
    try:
        res = requests.delete(WATCHLIST_URL, json={"mepID": mep_id})
        if res.status_code == 200:
            st.success("🗑️ MEP removed.")
            st.rerun()
        else:
            st.error(f"Remove failed: {res.text}")
    except Exception as e:
        st.error(f"Remove error: {e}")

# ---------- UI ----------

st.title("📊 MEP Watchlist")
st.markdown("This is your personal MEP dashboard. Bookmark notable MEPs all in one place.")

st.title("👀 Current Watchlist")
watchlist = get_watchlist()

if not watchlist:
    st.info("No MEPs in your watchlist yet.")
else:
    for mep in watchlist:
        with st.container():
            st.markdown("---")
            cols = st.columns([1, 3])
            with cols[0]:
                mep_id = mep.get("mepID")
                photo_url = f"https://www.europarl.europa.eu/mepphoto/{mep_id}.jpg" if mep_id else ""
                st.image(photo_url, width=100)
            with cols[1]:
                st.markdown(f"### {mep.get('name', 'Unnamed MEP')}")
                st.markdown(f"**🌍 Country**: {mep.get('countryOfOrigin', 'Unknown')}")
                st.markdown(f"**📊 Loyalty Score**: {mep.get('loyaltyScore', '?')}")
                st.markdown(f"**🏛️ Party ID**: {mep.get('partyID')}")
                if mep_id:
                    st.button(
                        "❌ Remove",
                        key=f"remove_{mep_id}_{mep['name']}",
                        on_click=remove_from_watchlist,
                        args=(mep_id,)
                    )

# Divider
st.markdown("## ➕ Add MEP to Watchlist")

all_meps = get_all_meps()
if all_meps:
    mep_options = {f"{mep['name']} ({mep['mepID']})": mep["mepID"] for mep in all_meps}
    selection = st.selectbox("Select MEP by name", list(mep_options.keys()))
    if st.button("Add Selected MEP"):
        add_to_watchlist(mep_options[selection])
else:
    st.warning("⚠️ No MEPs available.")