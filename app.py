from dash import Dash, dcc, html, Input, Output, callback, dash_table
import os
# https://dash.plotly.com/tutorial
import dash_leaflet as dl
# https://www.dash-leaflet.com/
from dash_extensions.javascript import arrow_function
import pandas as pd
import dash_bootstrap_components as dbc


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server

data_policy = pd.read_csv('data/Policy profiles.csv')

# https://green-deal-tracker-1b2ec05570ff.herokuapp.com/

#################################################### Layouts ########################################################

# Overview of the country
app.layout = html.Div([
    html.P('-------------- Header --------------'),
    html.P('European Green Deal Tracker Alpha'),

    
    # Navigation bar with levels or pages    
    html.P('-------------- Navi bar --------------'),
    html.Nav([
        html.P('Tracker'),
        html.P('Overview'),
    ]),
    
    html.P('-------------- Main content --------------'),
    html.H1('European Green Deal Tracker - Overview'),
    
    # Dropdown for country
    html.P('Country'),
    dcc.Dropdown(['EU', 'Sweden', 'Estonia'],
        'EU',
        id='dropdown-overview-country'
    ),
    
    # Dropdown for sector
    html.P('Sector'),
    dcc.Dropdown(['All', 'Climate', 'Energy', 'Transport', 'Industry', 'Environment and Oceans'],
        'All',
        id='dropdown-overview-sector'
    ),
    
    ############################# Table for country and sector #############################
    html.P(id='tbl_out'),

    
    
    # Map for implemented counties
    html.P('-------------- Map --------------'),

    html.P('This is the map for implemented countries, might be moved to another page'),
    dl.Map(children= [
        dl.TileLayer(), 
        # dl.GeoJSON(url="https://raw.githubusercontent.com/ansel-yu/SEI-green-deal-tracker/5c80f76182983f41fec8a3134b363f3dd06dc999/data/eu_2020.geojson?token=GHSAT0AAAAAACXVJWIWQCF7QORZ3XCF5UFCZYHY22Q", 
        #            zoomToBounds=False, id="map-eu-geojson", hideout=dict(selected=[])),
        dl.GeoJSON(url="data/ee_se_2020.geojson", 
                   zoomToBounds=False, id="map-working-country-geojson", hideout=dict(selected=[]), hoverStyle=arrow_function(dict(weight=5, color='#666', dashArray='')), zoomToBoundsOnClick=True),
        ], style={'height': '50vh'}, zoom=4, id='map-overview-country', center=[56.046467, 14.156450]),


    html.P('-------------- Text --------------'),

    html.Div(id='display-overview-country'),
    
    # dbc.Container([
    # dbc.Label('-------------- Filter out content --------------'),
    # dash_table.DataTable(data_policy.to_dict('records'),[{"name": i, "id": i} for i in data_policy[['name', 'full_name', 'country', 'sector']]], id='tbl'),
    # dbc.Alert(id='tbl_out'),
    # ]),
    

    
    
    
    html.Div(id='display-overview-sector'),


])



####################################################### Callback functions #####################################################

# Dropdown for country
@callback(Output('display-overview-country', 'children'), Input('dropdown-overview-country', 'value'))
def display_dropdown_value(value):
    return data_policy.loc[data_policy['country'] == value]['name']

# Dropdown for sector
@callback(Output('display-overview-sector', 'children'), Input('dropdown-overview-sector', 'value'))
def display_dropdown_value(value):
    return str(data_policy[data_policy['sector'] == value][['name']])

# Country + sector -> table
@callback(Output('tbl_out', 'children'), Input('dropdown-overview-sector', 'value'), Input('dropdown-overview-country', 'value'))
def change_table_dropdown_value(sector, country):
    return print(sector, country)


# Map for implemented counties
@app.callback(Output("map-overview-country", "formatOptions"), [Input("map-working-country-geojson", "clickData")], prevent_initial_call=True)
def load_country_on_map(click_data):
    print(click_data['properties']['NAME_ENGL'])
    # return click_data


# Interactive table
# @callback(Output('tbl_out', 'children'), Input('tbl', 'active_cell'))
# def update_graphs(active_cell):
#     return str(active_cell) if active_cell else "Click the table"


if __name__ == '__main__':
    app.run(debug=True)