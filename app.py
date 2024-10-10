from dash import Dash, dcc, html, Input, Output, callback
import os
# https://dash.plotly.com/tutorial
import dash_leaflet as dl
# https://www.dash-leaflet.com/
from dash_extensions.javascript import arrow_function


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server

#################################################### Layouts ########################################################

# Overview of the country
app.layout = html.Div([
    html.P('European Green Deal Tracker Alpha'),
    
    # Navigation bar with levels or pages    
    html.Nav([
        html.P('Tracker'),
        html.P('Overview'),
    ]),
    
    # Dropdown for country
    html.P('Country'),
    dcc.Dropdown(['EU', 'Sweden', 'Estonia'],
        'EU',
        id='dropdown-overview-country'
    ),
    html.Div(id='display-overview-country'),
    
    # Dropdown for sector
    html.P('Sector'),
    dcc.Dropdown(['All', 'Climate', 'Energy', 'Transport', 'Industry', 'Environment and Oceans'],
        'All',
        id='dropdown-overview-sector'
    ),
    html.Div(id='display-overview-sector'),
    
    # Map for implemented counties
    html.P('This is the map for implemented countries, might be moved to another page'),
    dl.Map(children= [
        dl.TileLayer(), 
        dl.GeoJSON(url="https://raw.githubusercontent.com/ansel-yu/SEI-green-deal-tracker/refs/heads/main/data/eu_2020.geojson?token=GHSAT0AAAAAACXVJWIWDWFULXKPGS5HEG7IZYHYPMA", 
                   zoomToBounds=False, id="map-eu-geojson", hideout=dict(selected=[]), hoverStyle=arrow_function(dict(weight=5, color='#666', dashArray=''))),
        dl.GeoJSON(url="https://raw.githubusercontent.com/ansel-yu/SEI-green-deal-tracker/refs/heads/main/data/ee_se_2020.geojson?token=GHSAT0AAAAAACXVJWIWDWFULXKPGS5HEG7IZYHYPMA", 
                   zoomToBounds=False, id="map-eu-geojson", hideout=dict(selected=[]), hoverStyle=arrow_function(dict(weight=5, color='#666', dashArray=''))),
        ], style={'height': '50vh'}, zoom=4, id='map-overview-country', center=[56.046467, 14.156450]),
])




####################################################### Callback functions #####################################################

# Dropdown for country
@callback(Output('display-overview-country', 'children'), Input('dropdown-overview-country', 'value'))
def display_dropdown_value(value):
    return f'You have selected {value}, NB: use as a variable later'

# Dropdown for sector
@callback(Output('display-overview-sector', 'children'), Input('dropdown-overview-sector', 'value'))
def display_dropdown_value(value):
    return f'You have selected {value}, NB: use as a variable later'

# Map for implemented counties
@app.callback(Output("map-overview-country", "formatOptions"), [Input("map-eu-geojson", "clickData")], prevent_initial_call=True)
def load_country_on_map(click_data):
    print(click_data['properties']['NAME_ENGL'])
    # return click_data



if __name__ == '__main__':
    app.run(debug=True)