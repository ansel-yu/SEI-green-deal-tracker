from dash import Dash, dcc, html, Input, Output, callback
import os
# https://dash.plotly.com/tutorial
import dash_leaflet as dl
# https://www.dash-leaflet.com/
from dash_extensions.javascript import arrow_function


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = Dash(__name__, external_stylesheets=external_stylesheets)

server = app.server

# Overview of the country
app.layout = html.Div([
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
    dcc.Dropdown(['Climate', 'Energy'],
        'Climate',
        id='dropdown-overview-sector'
    ),
    html.Div(id='display-overview-sector'),
    
    # Map for implemented counties
    dl.Map(children= [
        dl.TileLayer(), 
        dl.GeoJSON(url="https://raw.githubusercontent.com/leakyMirror/map-of-europe/refs/heads/master/GeoJSON/europe.geojson", zoomToBounds=True, id="map-eu-geojson",
               hideout=dict(selected=[]))
        ], style={'height': '50vh'}, center=[56, 10], zoom=6, id='map-overview-country'),
])

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
    print(click_data['properties']['NAME'])
    # return click_data



if __name__ == '__main__':
    app.run(debug=True)