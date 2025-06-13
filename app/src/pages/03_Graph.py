import logging
logger = logging.getLogger(__name__)

import streamlit as st
from modules.nav import SideBarLinks

st.set_page_config(layout = 'wide')

# Show appropriate sidebar links for the role of the currently logged in user
SideBarLinks()

# Example values
labels = ['ESN', 'The Left', 'Renew Europe', 'Remaining']
values = [25, 46, 77, 572]

# Create a full donut chart
fig = go.Figure(data=[go.Pie(
    labels=labels,
    values=values,
    hole=0.6,
    sort=False,
    direction='clockwise',
    rotation=180  # Rotates so it's a bottom half
)])

# Update to make it a semi-circle
fig.update_traces(textinfo='label+value', pull=[0, 0, 0, 0])
fig.update_layout(
    showlegend=True,
    margin=dict(t=0, b=0, l=0, r=0),
    height=400,
    width=700,
    annotations=[dict(text='148 / 720<br>Seats', x=0.5, y=0.25, font_size=14, showarrow=False)],
)

# Crop to semi-circle
fig.update_layout(
    piecolorway=['#636EFA', '#EF553B', '#00CC96', '#DDDDDD'],
    legend_orientation="h",
    legend=dict(x=0, y=-0.1),
)

fig.update_layout(
    # Clip to half the circle visually
    margin=dict(t=20, b=20),
    height=400
)
fig.update_traces(
    domain=dict(x=[0, 1], y=[0, 0.5])  # only bottom half is shown
)

fig.show()

