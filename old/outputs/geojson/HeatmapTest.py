import folium
from folium.plugins import HeatMap
import pandas as pd

# Load your data into a DataFrame
# Replace 'file_path' with the path to your CSV file
file_path = '/Users/peter/Desktop/MBW_Bluewater/data/BWB_AWQMP_Data_2009-2022_test.csv'
data = pd.read_csv(file_path)

# Your Mapbox token
token = "pk.eyJ1IjoicHd4dSIsImEiOiJjbHNqZW5pejQxbnB4MmxwcW9zMG5ucWo2In0._4ofEVzuOXcSbahAY4Skpw"  # Replace with your Mapbox access token
tileurl = f'https://api.mapbox.com/styles/v1/mapbox/satellite-streets-v12/tiles/256/{{z}}/{{x}}/{{y}}@2x?access_token={token}'

# Find the center of the map
latitude_center = data['latitude'].mean()
longitude_center = data['longitude'].mean()

# Create a map centered at the average location
m = folium.Map(location=[latitude_center, longitude_center], zoom_start=10, tiles=tileurl, attr='Mapbox')
map_folium = folium.Map(location=[latitude_center, longitude_center], zoom_start=10, tiles='OpenStreetMap')

tile = folium.TileLayer(
    tiles='https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}',
    attr='Esri',
    name='Esri Satellite',
    overlay=False,
    control=True
).add_to(map_folium)

# Prepare data for the HeatMap (latitude, longitude, and a weight parameter for depth)
heat_data = [[row['latitude'], row['longitude'], row['Total Water Depth (ft)']] for index, row in data.iterrows()]

# Create and add a HeatMap layer
HeatMap(heat_data, radius=25, gradient={0.4: 'blue', 0.65: 'lime', 1: 'red'}).add_to(m)

# Save the map to an HTML file
map_file_path = 'water_depth_heatmap_satellite.html'
m.save(map_file_path)

# The map is now using Mapbox satellite imagery as the base layer.
