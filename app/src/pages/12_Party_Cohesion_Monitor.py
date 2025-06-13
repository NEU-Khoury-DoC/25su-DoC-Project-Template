import streamlit as st
import requests
from sklearn.ensemble import RandomForestClassifier
from streamlit_extras.app_logo import add_logo
from modules.nav import SideBarLinks

SideBarLinks()

st.title("🧠 Party Dissent Predictor")
st.markdown("Use logistic regression to estimate dissent likelihood for EU parties.")

# --- Inputs ---
party = st.selectbox("Select a political party:", [
    'EPP', 'ESN', 'GUE/NGL', 'Greens/EFA', 'ID',
    'Patriots for Europe', 'Renew', 'S&D'
])

procedure_type = st.selectbox("Select a procedure type:", [
    'APP', 'BUD', 'BUI', 'CNS', 'COD', 'DEA', 'DEC', 'INI',
    'INL', 'NLE', 'REG', 'RPS', 'RSO', 'RSP'
])

# --- Predict button ---
if st.button("🔍 Predict Dissent Rate"):
    url = f"http://web-api:4000/l/prediction/{party}/{procedure_type}"
    
    try:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            st.success(f"📊 Predicted Dissent Rate: **{data['prediction']:.2f}%**")
        else:
            st.error("❌ Prediction failed. Try again or check the server.")
    except Exception as e:
        st.error(f"⚠️ Error: {e}")