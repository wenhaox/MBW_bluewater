""" import pandas as pd
import geopandas as gpd
import folium
import matplotlib.pyplot as plt

# Load data
file_path = 'BWB_AWQMP_Data_2009-2022.xlsx'
df = pd.read_excel(file_path, sheet_name='BWB Tidal Data 2009-2022')

# Convert to GeoDataFrame
gdf = gpd.GeoDataFrame(df, geometry=gpd.points_from_xy(df.longitude, df.latitude))

# Convert 'collection_date' to datetime
gdf['collection_date'] = pd.to_datetime(gdf['collection_date'])

# Create Folium map
map_center = [gdf['latitude'].mean(), gdf['longitude'].mean()]
folium_map = folium.Map(location=map_center, zoom_start=10)
for idx, row in gdf.iterrows():
    folium.Marker([row['latitude'], row['longitude']], 
                  popup=f"Station: {row['station_id']} Date: {row['collection_date']}").add_to(folium_map)

# Save map
map_file_path = "bwb_tidal_data_map.html"
folium_map.save(map_file_path)

# Time series analysis
gdf[['Total Nitrogen (mg/L)', 'Total Phosphorus (mg/L)', 'Chlorophyll (µg/L)']] = \
    gdf[['Total Nitrogen (mg/L)', 'Total Phosphorus (mg/L)', 'Chlorophyll (µg/L)']].apply(pd.to_numeric, errors='coerce')
time_series_data = gdf.groupby('collection_date').mean()

# Plot time series
plt.figure(figsize=(12, 6))
plt.plot(time_series_data['Total Nitrogen (mg/L)'], label='Total Nitrogen (mg/L)')
plt.plot(time_series_data['Total Phosphorus (mg/L)'], label='Total Phosphorus (mg/L)')
plt.plot(time_series_data['Chlorophyll (µg/L)'], label='Chlorophyll (µg/L)')
plt.xlabel('Date')
plt.ylabel('Measurement')
plt.title('Water Quality Measurements Over Time')
plt.legend()
plt.show()

map_file_path, gdf.head()  # Output file path and GeoDataFrame preview """
import dash
from dash import html, dcc
from dash.dependencies import Input, Output
import pandas as pd
import plotly.express as px

# Load data
file_path = 'BWB_AWQMP_Data_2009-2022.xlsx'
df = pd.read_excel(file_path, sheet_name='BWB Tidal Data 2009-2022')
df['collection_date'] = pd.to_datetime(df['collection_date'])

# Convert to numeric
measurements = [
    'Total Nitrogen (mg/L)', 'Total Phosphorus (mg/L)', 'Chlorophyll (µg/L)',
    'Total Kjeldahl Nitrogen (mg/L)', 'Enterococcus Bacteria (MPN/100mL) - A2LA Lab',
    'Enterococcus Bacteria (MPN/100mL) - BWB Lab', 'Secchi Depth (m)'
]
df[measurements] = df[measurements].apply(pd.to_numeric, errors='coerce')

# Initialize app
app = dash.Dash(__name__)

# Define layout
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

# Callback for map
@app.callback(
    Output('map-graph', 'figure'),
    [Input('nitrogen-graph', 'hoverData')]
)
def update_map(hoverData):
    fig_map = px.scatter_mapbox(df, lat='latitude', lon='longitude', hover_name='station_id',
                                color_continuous_scale=px.colors.cyclical.IceFire, size_max=15, zoom=10)
    fig_map.update_layout(mapbox_style="open-street-map")
    return fig_map

# Callbacks for graphs
@app.callback(
    Output('nitrogen-graph', 'figure'),
    [Input('map-graph', 'clickData')]
)
def update_nitrogen_graph(clickData):
    fig_nitrogen = px.line(df, x='collection_date', y='Total Nitrogen (mg/L)', title='Total Nitrogen Over Time')
    return fig_nitrogen

@app.callback(
    Output('phosphorus-graph', 'figure'),
    [Input('map-graph', 'clickData')]
)
def update_phosphorus_graph(clickData):
    fig_phosphorus = px.line(df, x='collection_date', y='Total Phosphorus (mg/L)', title='Total Phosphorus Over Time')
    return fig_phosphorus

@app.callback(
    Output('chlorophyll-graph', 'figure'),
    [Input('map-graph', 'clickData')]
)
def update_chlorophyll_graph(clickData):
    fig_chlorophyll = px.line(df, x='collection_date', y='Chlorophyll (µg/L)', title='Chlorophyll Over Time')
    return fig_chlorophyll

@app.callback(
    Output('kjeldahl-nitrogen-graph', 'figure'),
    [Input('map-graph', 'clickData')]
)
def update_kjeldahl_nitrogen_graph(clickData):
    fig_kjeldahl_nitrogen = px.line(df, x='collection_date', y='Total Kjeldahl Nitrogen (mg/L)', title='Total Kjeldahl Nitrogen Over Time')
    return fig_kjeldahl_nitrogen

@app.callback(
    Output('enterococcus-a2la-graph', 'figure'),
    [Input('map-graph', 'clickData')]
)
def update_enterococcus_a2la_graph(clickData):
    fig_enterococcus_a2la = px.line(df, x='collection_date', y='Enterococcus Bacteria (MPN/100mL) - A2LA Lab', title='Enterococcus Bacteria (A2LA Lab) Over Time')
    return fig_enterococcus_a2la

@app.callback(
    Output('enterococcus-bwb-graph', 'figure'),
    [Input('map-graph', 'clickData')]
)
def update_enterococcus_bwb_graph(clickData):
    fig_enterococcus_bwb = px.line(df, x='collection_date', y='Enterococcus Bacteria (MPN/100mL) - BWB Lab', title='Enterococcus Bacteria (BWB Lab) Over Time')
    return fig_enterococcus_bwb

@app.callback(
    Output('secchi-depth-graph', 'figure'),
    [Input('map-graph', 'clickData')]
)
def update_secchi_depth_graph(clickData):
    fig_secchi_depth = px.line(df, x='collection_date', y='Secchi Depth (m)', title='Secchi Depth Over Time')
    return fig_secchi_depth

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)



