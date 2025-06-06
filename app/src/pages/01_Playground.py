import logging
logger = logging.getLogger(__name__)

import streamlit as st
import requests
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
import pandas as pd
from modules.nav import SideBarLinks

# API Configuration
API_BASE_URL = "http://web-api:4000"  

# Page setup
st.set_page_config(layout='wide')
st.title("Data Playground")
st.markdown("*Explore how different economic factors affect income inequality.*")

# Sidebar
SideBarLinks()

# API Functions
@st.cache_data(ttl=300)  # Cache for 5 minutes
def fetch_available_features():
    """Fetch available feature variables from backend"""
    try:
        response = requests.get(f"{API_BASE_URL}/playground/features", timeout=10)
        if response.status_code == 200:
            return response.json().get("features", [])
        else:
            st.error(f"Failed to fetch features: {response.status_code}")
            return None
    except requests.exceptions.RequestException as e:
        st.error(f"Error connecting to backend: {str(e)}")
        return None

def save_graph_to_backend(user_id, graph_name, x_axis, x_min, x_max, x_steps, feature_values):
    """Save graph configuration to backend"""
    try:
        data = {
            "user_id": user_id,
            "name": graph_name,
            "x_axis": x_axis,
            "x_min": x_min,
            "x_max": x_max,
            "x_steps": x_steps,
            **feature_values  # Spread all feature values
        }
        
        response = requests.post(f"{API_BASE_URL}/playground/save", json=data, timeout=10)
        return response.status_code == 201, response.json()
    except requests.exceptions.RequestException as e:
        return False, {"error": str(e)}

@st.cache_data(ttl=60)  # Cache for 1 minute
def fetch_saved_graphs(user_id):
    """Fetch saved graphs for a user"""
    try:
        response = requests.get(f"{API_BASE_URL}/playground/saved/{user_id}", timeout=10)
        if response.status_code == 200:
            return response.json().get("saved_graphs", [])
        else:
            return []
    except requests.exceptions.RequestException:
        return []

def load_graph_from_backend(graph_id):
    """Load a specific graph configuration"""
    try:
        response = requests.get(f"{API_BASE_URL}/playground/graph/{graph_id}", timeout=10)
        if response.status_code == 200:
            return response.json()
        else:
            return None
    except requests.exceptions.RequestException:
        return None

# Feature variable mapping to match backend expectations
FEATURE_MAPPING = {
    "Population": "Population",
    "GDP per capita": "GDP_per_capita", 
    "Trade union density": "Trade_union_density",
    "Unemployment rate": "Unemployment_rate",
    "Health": "Health",
    "Education": "Education", 
    "Housing": "Housing",
    "Community development": "Community_development",
    "Productivity": "Productivity",
    "Real interest rates": "Real_interest_rates",
    "Corporate tax rate": "Corporate_tax_rate",
    "Inflation": "Inflation",
    "Personal/property tax": "Personal_property_tax",
    "IRLT": "IRLT"
}

# Global presets data - hardcoded for simplicity and performance
PRESETS = {
    "USA (2022)": {
        "Population": 331900000,
        "GDP_per_capita": 70248,
        "Trade_union_density": 10.3,
        "Unemployment_rate": 3.6,
        "Health": 8.8,
        "Education": 6.0,
        "Housing": 5.6,
        "Community_development": 7.2,
        "Productivity": 68.4,
        "Real_interest_rates": 2.4,
        "Corporate_tax_rate": 21.0,
        "Inflation": 8.0,
        "Personal_property_tax": 12.0,
        "IRLT": 0.42
    },
    "France (2022)": {
        "Population": 67750000,
        "GDP_per_capita": 42330,
        "Trade_union_density": 7.7,
        "Unemployment_rate": 7.3,
        "Health": 9.5,
        "Education": 5.5,
        "Housing": 6.8,
        "Community_development": 8.1,
        "Productivity": 67.1,
        "Real_interest_rates": 1.8,
        "Corporate_tax_rate": 25.0,
        "Inflation": 5.2,
        "Personal_property_tax": 18.5,
        "IRLT": 0.32
    },
    "Germany (2022)": {
        "Population": 83200000,
        "GDP_per_capita": 48720,
        "Trade_union_density": 16.7,
        "Unemployment_rate": 3.1,
        "Health": 9.7,
        "Education": 4.9,
        "Housing": 6.2,
        "Community_development": 8.3,
        "Productivity": 71.9,
        "Real_interest_rates": 1.5,
        "Corporate_tax_rate": 29.9,
        "Inflation": 6.9,
        "Personal_property_tax": 14.8,
        "IRLT": 0.29
    }
}

# Function to generate fake data for the graph
def generate_fake_gini_data(feature_name, x_min, x_max, steps):
    """Generate fake GINI coefficient data for demonstration - REPEATABLE"""
    
    # Create deterministic seed based on input parameters
    # This ensures same inputs always produce same outputs
    import hashlib
    seed_string = f"{feature_name}_{x_min}_{x_max}_{steps}"
    seed = int(hashlib.md5(seed_string.encode()).hexdigest()[:8], 16) % (2**31)
    np.random.seed(seed)
    
    x_values = np.linspace(x_min, x_max, steps)
    
    # Create realistic-looking fake GINI data based on feature type
    base_gini = 0.35  # Average GINI coefficient
    noise = np.random.normal(0, 0.02, len(x_values))  # Deterministic noise now
    
    # Different patterns based on feature type
    if "GDP" in feature_name or "capita" in feature_name:
        # GDP per capita typically has inverse relationship with inequality
        y_values = base_gini - (x_values - x_min) / (x_max - x_min) * 0.15 + noise
    elif "Unemployment" in feature_name:
        # Unemployment typically increases inequality
        y_values = base_gini + (x_values - x_min) / (x_max - x_min) * 0.12 + noise
    elif "Education" in feature_name or "Health" in feature_name:
        # Education and health spending typically reduce inequality
        y_values = base_gini - (x_values - x_min) / (x_max - x_min) * 0.10 + noise
    else:
        # Default pattern with slight upward trend
        y_values = base_gini + (x_values - x_min) / (x_max - x_min) * 0.08 + noise
    
    # Ensure GINI values stay within realistic bounds (0.2 to 0.6)
    y_values = np.clip(y_values, 0.2, 0.6)
    
    # Reset random state to avoid affecting other random operations
    np.random.seed(None)
    
    return x_values, y_values

# Initialize session state
if 'graph_data' not in st.session_state:
    st.session_state.graph_data = None
if 'available_features' not in st.session_state:
    st.session_state.available_features = None

# Check authentication and get user ID
if not st.session_state.get('authenticated', False):
    st.error("🔐 Please log in first!")
    st.info("👈 Use the sidebar to navigate to the home page and log in.")
    if st.button("🏠 Go to Home Page", type="primary"):
        st.switch_page('Home.py')
    st.stop()

# Get user ID from session state (set during login)
user_id = st.session_state.get('UserID')
if not user_id:
    st.error("❌ User ID not found in session. Please log in again.")
    if st.button("🏠 Go to Home Page", type="primary"):
        st.switch_page('Home.py')
    st.stop()

# Fetch available features from backend
if st.session_state.available_features is None:
    with st.spinner("Loading available features..."):
        backend_features = fetch_available_features()
        if backend_features:
            # Convert backend feature names to frontend display names
            display_features = []
            backend_to_display = {v: k for k, v in FEATURE_MAPPING.items()}
            
            for backend_feature in backend_features:
                display_name = backend_to_display.get(backend_feature, backend_feature)
                display_features.append(display_name)
            
            st.session_state.available_features = display_features
        else:
            # Fallback to hardcoded features if backend is unavailable
            st.session_state.available_features = list(FEATURE_MAPPING.keys())
            st.warning("⚠️ Backend unavailable - using default features")
#----------------------^^^^^^^^^^^^^^^^^^^^ Is this fetching of features from the backend necessary?


# vvvvvvvvvvvvvvvv Very cool but do we need for rn 
# Show current user info in sidebar
with st.sidebar:
    st.markdown("### 👤 Current User")
    user_name = st.session_state.get('Name', 'Unknown User')
    user_roles = st.session_state.get('Roles', [])
    
    st.info(f"**{user_name}**")
    if user_roles:
        st.caption(f"Roles: {', '.join(user_roles)}")
    
    # Logout button
    if st.button("🚪 Logout", use_container_width=True):
        # Clear session state
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.success("Logged out successfully!")
        st.switch_page('Home.py')
    
    st.markdown("---")
    
    # Load saved graphs
    st.markdown("### 📁 Saved Graphs")
    saved_graphs = fetch_saved_graphs(user_id)
    
    if saved_graphs:
        graph_names = [f"{graph['name']} ({graph['date_saved'][:10] if graph['date_saved'] else 'Unknown'})" 
                      for graph in saved_graphs]
        
        selected_graph = st.selectbox("Load saved graph:", ["None"] + graph_names, key="load_graph_select")
        
        if selected_graph != "None" and st.button("🔄 Load Graph", use_container_width=True):
            graph_index = graph_names.index(selected_graph)
            selected_graph_data = saved_graphs[graph_index]
            
            # Load graph configuration into session state
            st.session_state.loaded_graph = selected_graph_data
            # Clear any selected preset when loading a graph
            if 'selected_preset' in st.session_state:
                del st.session_state.selected_preset
            st.success(f"Loaded graph: {selected_graph_data['name']}")
            st.rerun()
    else:
        st.info("No saved graphs found")

# Main content area
if st.session_state.graph_data is not None:
    # Show the generated graph
    st.markdown("### Generated GINI Coefficient Prediction")
    
    # Create plotly figure
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=st.session_state.graph_data['x_values'],
        y=st.session_state.graph_data['y_values'],
        mode='lines+markers',
        name='GINI Prediction',
        line=dict(color='#1f77b4', width=3),
        marker=dict(size=6)
    ))
    
    fig.update_layout(
        title=f"GINI Coefficient vs {st.session_state.graph_data['feature_name']}",
        xaxis_title=st.session_state.graph_data['feature_name'],
        yaxis_title='GINI Coefficient',
        template='plotly_white',
        height=500,
        hovermode='x unified'
    )
    
    st.plotly_chart(fig, use_container_width=True)
else:
    # Show placeholder image when no graph is generated
    st.image("assets/posts/placeholderGraph.gif", caption="GINI vs Population (example)")

# Columns for presets + controls
col1, col2, col3 = st.columns([0.75, 0.05, 0.2])

with col1:
    st.markdown("### Presets:")
    
    preset_options = ["None"] + list(PRESETS.keys())
    selected_preset = st.selectbox("", preset_options, key="preset_select")
    
    # Apply preset button
    if selected_preset != "None" and st.button("📋 Apply Preset", use_container_width=True):
        # Store the selected preset data in session state
        st.session_state.selected_preset = PRESETS[selected_preset]
        st.success(f"Applied preset: {selected_preset}")
        st.rerun()

    st.markdown("")

    # Feature buttons — 4x4 grid to accommodate all features
    st.markdown("### Feature Variables:")
    feature_cols = st.columns(4)

    # Determine default values (priority: loaded graph > selected preset > hardcoded defaults)
    loaded_graph = st.session_state.get('loaded_graph', None)
    selected_preset_data = st.session_state.get('selected_preset', None)
    
    def get_default_value(feature_key, fallback_default):
        """Get default value with priority: loaded graph > preset > fallback"""
        if loaded_graph and 'features' in loaded_graph:
            return loaded_graph['features'].get(feature_key, fallback_default)
        elif selected_preset_data:
            return selected_preset_data.get(feature_key, fallback_default)
        else:
            return fallback_default

    with feature_cols[0]:
        population = st.number_input("Population:", 
                                   value=get_default_value('Population', 300000000), 
                                   key="population")
        gdp_per_capita = st.number_input("GDP per capita:", 
                                       value=get_default_value('GDP_per_capita', 50000), 
                                       key="gdp_per_capita")
        trade_union = st.number_input("Trade union density:", 
                                    value=get_default_value('Trade_union_density', 10.5), 
                                    key="trade_union")
        unemployment = st.number_input("Unemployment rate:", 
                                     value=get_default_value('Unemployment_rate', 5.2), 
                                     key="unemployment")

    with feature_cols[1]:
        health = st.number_input("Health:", 
                               value=get_default_value('Health', 8.0), 
                               key="health")
        education = st.number_input("Education:", 
                                  value=get_default_value('Education', 7.5), 
                                  key="education")
        housing = st.number_input("Housing:", 
                                value=get_default_value('Housing', 6.8), 
                                key="housing")
        community = st.number_input("Community development:", 
                                  value=get_default_value('Community_development', 7.2), 
                                  key="community")

    with feature_cols[2]:
        productivity = st.number_input("Productivity:", 
                                     value=get_default_value('Productivity', 95.0), 
                                     key="productivity")
        real_interest = st.number_input("Real interest rates:", 
                                      value=get_default_value('Real_interest_rates', 2.5), 
                                      key="real_interest")
        corporate_tax = st.number_input("Corporate tax rate:", 
                                      value=get_default_value('Corporate_tax_rate', 21), 
                                      key="corporate_tax")
        inflation = st.number_input("Inflation:", 
                                  value=get_default_value('Inflation', 2.1), 
                                  key="inflation")

    with feature_cols[3]:
        personal_tax = st.number_input("Personal/property tax:", 
                                     value=get_default_value('Personal_property_tax', 15), 
                                     key="personal_tax")
        irlt = st.number_input("IRLT:", 
                             value=get_default_value('IRLT', 0.0), 
                             key="irlt")
        # Add some spacing for visual balance
        st.markdown("")
        st.markdown("")

with col3:
    st.markdown("### Currently Comparing:")
    
    # Use features from backend if available
    available_features = st.session_state.available_features or list(FEATURE_MAPPING.keys())
    
    # Set default compare feature from loaded graph
    default_compare_feature = None
    if loaded_graph:
        backend_feature = loaded_graph.get('x_axis')
        backend_to_display = {v: k for k, v in FEATURE_MAPPING.items()}
        default_compare_feature = backend_to_display.get(backend_feature)
    
    default_index = 0
    if default_compare_feature and default_compare_feature in available_features:
        default_index = available_features.index(default_compare_feature)
    
    compare_feature = st.selectbox("Feature", available_features, 
                                 index=default_index, key="compare_feature")

    # Set default values from loaded graph
    default_x_min = loaded_graph.get('x_min', 0.0) if loaded_graph else 0.0
    default_x_max = loaded_graph.get('x_max', 100.0) if loaded_graph else 100.0
    default_steps = loaded_graph.get('x_steps', 20) if loaded_graph else 20

    x_min = st.number_input("Min:", value=float(default_x_min), key="x_min")
    x_max = st.number_input("Max:", value=float(default_x_max), key="x_max")
    steps = st.number_input("Steps:", value=int(default_steps), min_value=5, max_value=100, key="steps")
    
    st.markdown("")
    
    # Generate button
    if st.button("🚀 Generate Graph", type="primary", use_container_width=True):
        if x_min >= x_max:
            st.error("Min value must be less than Max value!")
        elif steps < 5:
            st.error("Steps must be at least 5!")
        else:
            # Generate fake data
            with st.spinner("Generating predictions..."):
                x_values, y_values = generate_fake_gini_data(compare_feature, x_min, x_max, int(steps))

                # Store in session state
                st.session_state.graph_data = {
                    'x_values': x_values,
                    'y_values': y_values,
                    'feature_name': compare_feature
                }
                
                st.success("Graph generated successfully!")
                st.rerun()
    
    # Save button
    if st.session_state.graph_data is not None:
        st.markdown("")
        graph_name = st.text_input("Graph name:", placeholder="My Graph", key="graph_name_input")
        
        if st.button("💾 Save Graph", use_container_width=True) and graph_name:
            # Collect all feature values
            feature_values = {
                FEATURE_MAPPING["Population"]: population,
                FEATURE_MAPPING["GDP per capita"]: gdp_per_capita,
                FEATURE_MAPPING["Trade union density"]: trade_union,
                FEATURE_MAPPING["Unemployment rate"]: unemployment,
                FEATURE_MAPPING["Health"]: health,
                FEATURE_MAPPING["Education"]: education,
                FEATURE_MAPPING["Housing"]: housing,
                FEATURE_MAPPING["Community development"]: community,
                FEATURE_MAPPING["Productivity"]: productivity,
                FEATURE_MAPPING["Real interest rates"]: real_interest,
                FEATURE_MAPPING["Corporate tax rate"]: corporate_tax,
                FEATURE_MAPPING["Inflation"]: inflation,
                FEATURE_MAPPING["Personal/property tax"]: personal_tax,
                FEATURE_MAPPING["IRLT"]: irlt,
                # Add region features with default values
                "Region_East_Asia_and_Pacific": 0,
                "Region_Europe_and_Central_Asia": 0,
                "Region_Latin_America_and_Caribbean": 0,
                "Region_Middle_East_and_North_Africa": 0,
            }
            
            backend_feature_name = FEATURE_MAPPING.get(compare_feature, compare_feature)
            
            with st.spinner("Saving graph..."):
                success, response = save_graph_to_backend(
                    user_id, 
                    graph_name, 
                    backend_feature_name,
                    x_min, x_max, steps,
                    feature_values
                )
                
                if success:
                    st.success(f"Graph '{graph_name}' saved successfully!")
                    # Clear the cached saved graphs so they refresh
                    st.cache_data.clear()
                else:
                    st.error(f"Failed to save graph: {response.get('error', 'Unknown error')}")
    
    # Clear button
    if st.button("🗑️ Clear Graph", use_container_width=True):
        st.session_state.graph_data = None
        if 'loaded_graph' in st.session_state:
            del st.session_state.loaded_graph
        st.rerun()