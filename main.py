from pathlib import Path
import argparse

import pandas as pd
from dash import html, dcc, Dash
from dash.dependencies import Input, Output
import plotly.express as px

from lib import load_data


app = Dash(__name__)

app.layout = html.Div([
    html.H1("Water Quality Data Visualization"),
    dcc.Graph(id='map-graph'),
    dcc.Graph(id='nitrogen-graph'),
    dcc.Graph(id='phosphorus-graph'),
    dcc.Graph(id='chlorophyll-graph'),
    dcc.Graph(id='kjeldahl-nitrogen-graph'),
    dcc.Graph(id='enterococcus-a2la-graph'),
    dcc.Graph(id='enterococcus-bwb-graph'),
    dcc.Graph(id='secchi-depth-graph')
])

df = load_data('./data/BWB_AWQMP_Data_2009-2022.xlsx', 'BWB Tidal Data 2009-2022')


@app.callback(
    Output('map-graph', 'figure'),
    [Input('nitrogen-graph', 'hoverData')]
)
def update_map(hoverData):
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
    Output('nitrogen-graph', 'figure'),
    [Input('map-graph', 'clickData')]
)
def update_nitrogen_graph(clickData):
    fig_nitrogen = px.line(df,
                           x='collection_date',
                           y='Total Nitrogen (mg/L)',
                           title='Total Nitrogen Over Time')
    return fig_nitrogen

@app.callback(
    Output('phosphorus-graph', 'figure'),
    [Input('map-graph', 'clickData')]
)
def update_phosphorus_graph(clickData):
    fig_phosphorus = px.line(df,
                             x='collection_date',
                             y='Total Phosphorus (mg/L)',
                             title='Total Phosphorus Over Time')
    return fig_phosphorus

@app.callback(
    Output('chlorophyll-graph', 'figure'),
    [Input('map-graph', 'clickData')]
)
def update_chlorophyll_graph(clickData):
    fig_chlorophyll = px.line(df,
                              x='collection_date',
                              y='Chlorophyll (µg/L)',
                              title='Chlorophyll Over Time')
    return fig_chlorophyll

@app.callback(
    Output('kjeldahl-nitrogen-graph', 'figure'),
    [Input('map-graph', 'clickData')]
)
def update_kjeldahl_nitrogen_graph(clickData):
    fig_kjeldahl_nitrogen = px.line(df,
                                    x='collection_date',
                                    y='Total Kjeldahl Nitrogen (mg/L)',
                                    title='Total Kjeldahl Nitrogen Over Time')
    return fig_kjeldahl_nitrogen

@app.callback(
    Output('enterococcus-a2la-graph', 'figure'),
    [Input('map-graph', 'clickData')]
)
def update_enterococcus_a2la_graph(clickData):
    fig_enterococcus_a2la = px.line(df,
                                    x='collection_date',
                                    y='Enterococcus Bacteria (MPN/100mL) - A2LA Lab',
                                    title='Enterococcus Bacteria (A2LA Lab) Over Time')
    return fig_enterococcus_a2la

@app.callback(
    Output('enterococcus-bwb-graph', 'figure'),
    [Input('map-graph', 'clickData')]
)
def update_enterococcus_bwb_graph(clickData):
    fig_enterococcus_bwb = px.line(df,
                                   x='collection_date',
                                   y='Enterococcus Bacteria (MPN/100mL) - BWB Lab',
                                   title='Enterococcus Bacteria (BWB Lab) Over Time')
    return fig_enterococcus_bwb

@app.callback(
    Output('secchi-depth-graph', 'figure'),
    [Input('map-graph', 'clickData')]
)
def update_secchi_depth_graph(clickData):
    fig_secchi_depth = px.line(df,
                               x='collection_date',
                               y='Secchi Depth (m)',
                               title='Secchi Depth Over Time')
    return fig_secchi_depth

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--debug', action='store_true')
    return parser.parse_args()

def run():
    args = parse_args()
    app.run_server(debug=args.debug)

if __name__ == "__main__":
    run()
