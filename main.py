from pathlib import Path
import argparse

import pandas as pd
from dash import html, dcc, Dash
from dash.dependencies import Input, Output
import plotly.express as px
import dash
import dash_bootstrap_components as dbc

from lib import load_data

app = dash.Dash()

df = load_data('./data/BWB_AWQMP_Data_2009-2022.xlsx', 'BWB Tidal Data 2009-2022')
df['collection_date'] = pd.to_datetime(df['collection_date']) 

app.layout = html.Div([
    html.H1("Water Quality Data Visualization", style={'font-family': 'Roboto, sans-serif', 'color': '#003366'}),

    html.Div([
        html.Div([
            dcc.Graph(id='map-graph', style={'height': '90vh'}),  
            html.Button('Play', id='play-button', n_clicks=0),
            html.Button('Pause', id='pause-button', n_clicks=0),
            dcc.Interval(id='interval-component', interval=1*1000, disabled=True),
            dcc.Store(id='date-index', data=0), 

        ], style={'width': '50%', 'display': 'inline-block', 'height': '90vh'}),  


        html.Div([
            dcc.Dropdown(
                id='graph-type-dropdown',
                options=[
                    {'label': 'Total Nitrogen', 'value': 'nitrogen'},
                    {'label': 'Total Phosphorus', 'value': 'phosphorus'},
                    {'label': 'Chlorophyll', 'value': 'chlorophyll'},
                    {'label': 'Total Kjeldahl Nitrogen', 'value': 'kjeldahl_nitrogen'},
                    {'label': 'Enterococcus A2LA', 'value': 'enterococcus_a2la'},
                    {'label': 'Enterococcus BWB', 'value': 'enterococcus_bwb'},
                    {'label': 'Secchi Depth', 'value': 'secchi_depth'}
                ],
                value='nitrogen',
                style={'font-family': 'Roboto, sans-serif'}
            ),
            dcc.Graph(id='main-graph', style={'height': '85vh'}),  
        ], style={'width': '50%', 'display': 'inline-block', 'vertical-align': 'top', 'height': '90vh', 'font-family': 'Roboto, sans-serif', 'color': '#005662', 'background-color': '#e6fff5'}),  
    ], style={'height': '90vh', 'font-family': 'Roboto, sans-serif'})
])

@app.callback(
    Output('map-graph', 'figure'),
    [Input('graph-type-dropdown', 'value')]
)
def update_map(graph_type):
    fig_map = px.scatter_mapbox(df,
                                lat='latitude',
                                lon='longitude',
                                hover_name='station_id',
                                color_continuous_scale=px.colors.cyclical.IceFire,
                                size_max=15,
                                zoom=10)
    fig_map.update_layout(mapbox_style="open-street-map")
    return fig_map

@app.callback(
    Output('main-graph', 'figure'),
    [Input('graph-type-dropdown', 'value')]
)
def update_graph(graph_type):
    y_axis = {
        'nitrogen': 'Total Nitrogen (mg/L)',
        'phosphorus': 'Total Phosphorus (mg/L)',
        'chlorophyll': 'Chlorophyll (µg/L)',
        'kjeldahl_nitrogen': 'Total Kjeldahl Nitrogen (mg/L)',
        'enterococcus_a2la': 'Enterococcus Bacteria (MPN/100mL) - A2LA Lab',
        'enterococcus_bwb': 'Enterococcus Bacteria (MPN/100mL) - BWB Lab',
        'secchi_depth': 'Secchi Depth (m)'
    }.get(graph_type, 'Total Nitrogen (mg/L)')

    title = f"{y_axis.split('(')[0]}Over Time"

    return px.line(df, x='collection_date', y=y_axis, title=title)

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--debug', action='store_true')
    return parser.parse_args()

def run():
    args = parse_args()
    app.run_server(debug=args.debug)

if __name__ == "__main__":
    run()