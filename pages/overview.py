import dash
from dash import Dash, dcc, html, Input, Output, callback, dash_table
import os
# https://dash.plotly.com/tutorial
import dash_leaflet as dl
# https://www.dash-leaflet.com/
from dash_extensions.javascript import arrow_function
import pandas as pd
import dash_bootstrap_components as dbc


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
dash.register_page(__name__)

data_policy = pd.read_csv('data/Policy profiles.csv')

# https://green-deal-tracker-1b2ec05570ff.herokuapp.com/

#################################################### Layouts ########################################################

# Overview of the country
layout = html.Div([
    html.P('-------------- Title bar --------------'),
    html.P('European Green Deal Tracker - Overview'),

    
    # Navigation bar with levels or pages    
    # html.P('-------------- Navi bar --------------'),
    # html.Div([
    #     html.Div([
    #         html.Div(
    #             dcc.Link(f"{page['name']} - {page['path']}", href=page["relative_path"])
    #         ) for page in dash.page_registry.values()
    #     ]),    
    #     dash.page_container,
    # ]),
    
    # html.Nav([
    #     html.P('Home'),
    #     html.P('Overview'),
    # ]),
    
    html.P('-------------- Main content --------------'),
    
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
    
    # Dropdown for policy
    # html.P('Policy measures'),
    # dcc.Dropdown(data_policy['full_name'].unique().tolist(),
    #     None,
    #     id='dropdown-overview-policy'
    # ),
    
    # Map for implemented counties
    # html.P('-------------- Map --------------'),
    # html.Div([
    #     dl.Map(style={'height': '50vh'}, zoom=4, id='map-overview', center=[56.046467, 14.156450], children= [
    #         dl.TileLayer(),
    #         # dl.GeoJSON(url="https://raw.githubusercontent.com/ansel-yu/SEI-green-deal-tracker/refs/heads/main/data/eu_2020.json", 
    #         #         zoomToBounds=False, id="map-eu-geojson"),
    #         dl.GeoJSON(url="https://raw.githubusercontent.com/ansel-yu/SEI-green-deal-tracker/refs/heads/main/data/ee_se_2020.geojson", 
    #                 zoomToBounds=False, id="map-working-country-geojson", hideout=dict(selected=[]), hoverStyle=arrow_function(dict(weight=5, color='#666', dashArray='')), zoomToBoundsOnClick=True),
    #         ], 
    #         ),
    # ], style={'width': '40%', 'height': '50vh'}),


    # html.P('-------------- Text of country specific policies --------------'),
    # html.Div(id='display-overview-country'),
    
    
    # html.P('-------------- Text of sector specific policies --------------'),
    # html.Div(id='display-overview-sector'),

    html.P('-------------- Country intro --------------'),
    html.Div(id='intro-country'),

    html.P('-------------- Table for country and sector --------------'),
    dash_table.DataTable(id='tbl-overview-sector-country'),

    html.P('-------------- Text of clicked item --------------'),
    html.Div(id='tbl-overview-sector-country-out'),

])



####################################################### Callback functions #####################################################

# Dropdown for country -> intro
@callback(Output('intro-country', 'children'), Input('dropdown-overview-country', 'value'))
def display_dropdown_value(country):
    if country == 'EU':
        return 'EU is the best'
    elif country == 'Sweden':
        return 'Sweden is the best'
    elif country == 'Estonia':
        return 'Estonia is the best'

# # Dropdown for sector
# @callback(Output('display-overview-sector', 'children'), Input('dropdown-overview-sector', 'value'))
# def display_dropdown_value(sector):
#     return data_policy[data_policy['sector'] == sector]['name']

# Country + sector -> table
@callback([Output('tbl-overview-sector-country', component_property='data'), Output('tbl-overview-sector-country', component_property='columns')],
          [Input('dropdown-overview-sector', 'value'), Input('dropdown-overview-country', 'value')])
def change_table_dropdown_value(sector, country):
    
    if sector == 'All':
        df = data_policy[(data_policy['country'] == country)][['full_name', 'country', 'hindering_factors', 'enabling_factors', 'application_date', 'implementation_status']]
    elif country == 'EU':
        df = data_policy[(data_policy['sector'] == sector)][['full_name', 'country', 'hindering_factors', 'enabling_factors', 'application_date', 'implementation_status']]
    else:
        df = data_policy[(data_policy['sector'] == sector) & (data_policy['country'] == country)][['full_name', 'hindering_factors', 'enabling_factors', 'application_date', 'implementation_status']]
    columns = [{'name': col, 'id': col} for col in df.columns]
    data = df.to_dict('records')
    return data, columns

# Table -> text
@callback(Output('tbl-overview-sector-country-out', 'children'), Input('tbl-overview-sector-country', 'active_cell'))
def update_graphs(active_cell):
    return str(active_cell) if active_cell else "Click the table"


# Policy -> table
# @callback([Output('tbl-overview-policy', component_property='data'), Output('tbl-overview-policy', component_property='columns')],
#           [Input('dropdown-overview-policy', 'value')])
# def change_table_dropdown_value(policy):
#     df = data_policy[(data_policy['full_name'] == policy)][['country', 'hindering_factors', 'enabling_factors', 'implementation_status']]
#     columns = [{'name': col, 'id': col} for col in df.columns]
#     data = df.to_dict('records')
#     return data, columns
    # return print(sector, country)


# Map for implemented counties
# @callback(Output("map-overview", "formatOptions"), [Input("map-working-country-geojson", "clickData")], prevent_initial_call=True)
# def load_country_on_map(click_data):
#     print(click_data['properties']['NAME_ENGL'])
    # return click_data


# Map to filter out the clicked counties
# @callback(Output('display-overview-country', 'children'), [Input("map-working-country-geojson", "clickData")], prevent_initial_call=True)
# def load_country_on_map(click_data):
#     # print(click_data['properties']['NAME_ENGL'])
#     return data_policy.loc[data_policy['country'] == str(click_data['properties']['NAME_ENGL'])]['name']


