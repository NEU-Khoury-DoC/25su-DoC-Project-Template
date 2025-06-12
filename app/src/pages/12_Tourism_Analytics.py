import logging
logger = logging.getLogger(__name__)
import streamlit as st
import requests
from streamlit_extras.app_logo import add_logo
from modules.nav import SideBarLinks
from pages.styling_pages import offical_font
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
#import kaleido

SideBarLinks()


def data_sorting(data): 
    data["Value"] = pd.to_numeric(data["Score"], errors="coerce")
    new_data = data.sort_values(by="Score")
    return new_data

def get_tourism_prior_graph(tourism_df):

    data_19 = tourism_df.groupby("TourismYear").get_group(2019)
    data_21 = tourism_df.groupby("TourismYear").get_group(2021)
    data_24 = tourism_df.groupby("TourismYear").get_group(2024)

    new_19 = data_sorting(data_19)
    country_19 = new_19["Country"]
    values_19 = new_19["Score"]

    new_21 = data_sorting(data_21)
    country_21 = new_21["Country"]
    values_21 = new_21["Score"]

    new_24 = data_sorting(data_24)
    country_24 = new_24["Country"]
    values_24 = new_24["Score"]

    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=values_19.astype(float),
        y= country_19,
        name= '2019' ,
        marker_color='indianred', 
        orientation = "h"
    ))
    fig.add_trace(go.Bar(
        x=values_21.astype(float),
        y=country_21,
        name='2021',
        marker_color='lightsalmon', 
        orientation = "h"
    ))
    fig.add_trace(go.Bar(
        x=values_24.astype(float),
        y= country_24,
        name='2024',
        marker_color='pink', 
        orientation = "h"
    ))

    # Here we modify the tickangle of the xaxis, resulting in rotated labels.
    fig.update_layout(barmode='group', height= 10* 81, title = "Prioritization of Travel and Tourism")
    fig.update_layout(
        title={
            "text": "Country Priotization of Travel and Tourism Score (1-7).png",
            "x": 0.5,
            "xanchor": "center"
        },
        height=10* 81,
        width=900,
        xaxis_title= 'Score (1-7)'
    )
    return fig


def get_road_spending_graph(final_gdp_roadspending_df):
    gdp = final_gdp_roadspending_df['GDP']
    road_spend = final_gdp_roadspending_df['RoadSpending']
    country = final_gdp_roadspending_df["Country"]
    year = final_gdp_roadspending_df['SpendingYear']
    df = final_gdp_roadspending_df

    fig = px.scatter(df, x=gdp, y=road_spend, animation_frame=year, size=gdp, color=country,
            hover_name=country, log_x=True, size_max=60, range_x=[5e+9,6e+12], range_y=[(-1000000000),2.5e+10],
            color_discrete_sequence=px.colors.qualitative.Alphabet)

    # Hide all countries except Hungary
    fig.for_each_trace(
        lambda trace: trace.update(visible='legendonly') if trace.name != 'Hungary' else trace.update(visible=True)
    )

    fig.update_layout(
        xaxis_title="GDP",
        yaxis_title="Road Spending", 
        title={
            "text": "Country GDP vs. Road Spending (1995-2023)",
            "x": 0.5,
            "xanchor": "center"
        }
    )
    return fig

def get_trips_graph(start_df, country):
    final_1plus_df = start_df.groupby(['Country', 'TripYear'], as_index = False)['NumTrips'].sum()
    final_1plus_df['Purpose'] = 'Personal Reasons'
    final_1plus_df['Duration'] = '1 night or over'

    final_1plus_df = final_1plus_df[['Purpose', 'Duration', 'Country', 'TripYear', 'NumTrips']]

    # Plot the line graph
    fig = px.line(final_1plus_df, x='TripYear', y='NumTrips', color='Country', 
                color_discrete_sequence=px.colors.qualitative.Alphabet,)

    # Set all countries to 'legendonly' (hidden but clickable) except Hungary
    fig.for_each_trace(
        lambda trace: trace.update(visible='legendonly') if trace.name != st.session_state["Nationality"] else trace.update(visible=True)
    )

    fig.update_layout(title='Number of Trips (1 Plus Nights) per Year by Country',
                    xaxis_title='TripYear',
                    yaxis_title='Number of Trips',
                    legend_title='Country')
    
    return fig

def tourism_official_data_tables():
    offical_font("Tourism Infrastructure Analytics", False)
    BASE_URL = "http://host.docker.internal:4000/official"
    tables = {
        "Road Quality": {
            "endpoint": "/roadquality",
            "description": """This dataset tracks road infrastructure quality scores for different countries
              across multiple years, providing a standardized assessment of each nation's road network condition. 
              The quality scores enable year over year comparisons of road infrastructure improvements or deterioration 
              within countries and benchmarking across different nations."""
        },
        "Tourism Prioritization": {
            "endpoint": "/tourismprioritization",
            "description": """This graph shows government tourism prioritization scores by country and year, 
            indicating how much emphasis each nation places on developing and promoting its tourism sector, 
            and how it has changed over time."""
        },
        "Road Spending": {
            "endpoint": "/roadspending",
            "description": """This graph tracks government road infrastructure spending by country and year, 
            capturing both absolute spending amounts and each nation's GDP to calculate road investment as 
            a percentage of economic output. It enables analysis of infrastructure investment trends 
            over time within countries and allows for meaningful comparisons of road spending priorities 
            across nations regardless of economic size."""
        },
        "Trips": {
            "endpoint": "/trips",
            "description": """This graph records tourism trip volumes by country and year, for stays of 1 night or more.
            The line plot helps analyze tourism patterns and preferences to help national officials understand
            the recent history of tourism in their country."""
        }
    }
    
    def fetch_data(endpoint):
        try:
            response = requests.get(f"{BASE_URL}{endpoint}")
            if response.status_code == 200:
                data = response.json()
                return data, None
            else:
                return None, f"API Error: {response.status_code}"
        except requests.exceptions.RequestException as e:
            return None, f"Connection Error: {str(e)}"
        except Exception as e:
            return None, f"Error: {str(e)}"
    
    tab_names = list(tables.keys())
    tabs = st.tabs([f"{name}" for name in tab_names])
    
    for i, (table_name, table_info) in enumerate(tables.items()):
        with tabs[i]:
            st.subheader(f"{table_name}")
            st.markdown(f"*{table_info['description']}*")
            with st.spinner(f"Loading {table_name} data..."):
                data, error = fetch_data(table_info['endpoint'])
                if error:
                    st.error(f"Failed to load data: {error}")
                elif data:
                    try:
                        df = pd.DataFrame(data)
                        if not df.empty:
                            col1, col2 = st.columns(2)
                            
                            # with col1:
                            #     if 'Country' in df.columns:
                            #         available_countries = sorted(df['Country'].unique())
                            #         selected_countries = st.multiselect(
                            #             "Select Countries:",
                            #             options=available_countries,
                            #             default=[],
                            #             key=f"countries_{table_name}"
                            #         )
                            #     else:
                            #         selected_countries = []
                            
                            # with col2:
                            #     year_columns = [col for col in df.columns if 'year' in col.lower() or 'Year' in col]
                            #     if year_columns:
                            #         year_column = year_columns[0]
                            #         available_years = sorted(df[year_column].unique())
                            #         selected_years = st.multiselect(
                            #             "Select Years:",
                            #             options=available_years,
                            #             default=[],
                            #             key=f"years_{table_name}"
                            #         )
                            #     else:
                            #         selected_years = []
                            #         year_column = None
                            
                            # filtered_df = df.copy()
                            # if selected_countries and 'Country' in df.columns:
                            #     filtered_df = filtered_df[filtered_df['Country'].isin(selected_countries)]
                            # if selected_years and year_column:
                            #     filtered_df = filtered_df[filtered_df[year_column].isin(selected_years)]

                            cur_graph = None

                            if table_info["endpoint"] == "/roadquality":
                                print("RoadQuality")
                                
                            elif table_info["endpoint"] == "/tourismprioritization":
                                cur_graph = get_tourism_prior_graph(df)
                            
                            elif table_info["endpoint"] == "/roadspending":
                                cur_graph = get_road_spending_graph(df)

                            elif table_info["endpoint"] == "/trips":
                                cur_graph = get_trips_graph(df, st.session_state["Nationality"])

                            st.plotly_chart(cur_graph, use_container_width=True)

                        else:
                            st.warning(f"No data available in {table_name}")
                    except Exception as e:
                        st.error(f"Error processing data: {str(e)}")
                else:
                    st.warning(f"No data returned from {table_name} endpoint")

tourism_official_data_tables()