import pandas as pd
import folium
from folium.plugins import HeatMapWithTime
import os
import numpy as np
from sklearn.preprocessing import MinMaxScaler
import geopandas as gpd
from shapely.geometry import Point
from geopandas import GeoDataFrame

# Load CSV data
df = pd.read_csv('animated heatmap/processed data/predicted_kriged_bacteria_levels.csv')

# Create 'collection_date' column
df['collection_date'] = pd.to_datetime(df[['year', 'month']].assign(DAY=1))

# Specify your start and end dates here
start_date = pd.to_datetime('2011-05-01')
end_date = pd.to_datetime('2011-12-01') 

# Filter the dataframe by date range
filtered_df = df[(df['collection_date'] >= start_date) & (df['collection_date'] <= end_date)]

# Normalize 'predicted_value'
bacteria_levels = filtered_df['predicted_value'].values.reshape(-1, 1)
scaler = MinMaxScaler(feature_range=(0, 1))
normalized_bacteria_levels = scaler.fit_transform(bacteria_levels)
filtered_df = filtered_df.copy()
filtered_df['normalized_value'] = normalized_bacteria_levels.flatten()

# Load Chesapeake Bay boundary GeoJSON file
chesapeake_bay_boundary = gpd.read_file('path_to_your_chesapeake_bay_boundary_file.geojson')

# Convert DataFrame to GeoDataFrame
gdf = GeoDataFrame(filtered_df, geometry=gpd.points_from_xy(filtered_df.longitude, filtered_df.latitude))

# Perform spatial join to filter points within the Chesapeake Bay boundary
points_within_chesapeake = gpd.sjoin(gdf, chesapeake_bay_boundary, how='inner', op='within')

# Prepare data for HeatMapWithTime
data_per_date = []
dates = []

for date in np.sort(points_within_chesapeake['collection_date'].unique()):
    date = pd.to_datetime(date).to_pydatetime()
    day_data = points_within_chesapeake[points_within_chesapeake['collection_date'] == date]
    heat_data = day_data[['latitude', 'longitude', 'normalized_value']].values.tolist()
    data_per_date.append(heat_data)
    dates.append(date.strftime('%Y-%m-%d'))

# Initialize map at Baltimore, MD.
m = folium.Map(location=[39.2904, -76.6122], zoom_start=9)

# Custom gradient
gradient = {
    0.0: 'blue', 
    0.05: 'cyan', 
    0.1: 'lime', 
    0.2: 'yellow', 
    0.3: 'orange', 
    0.4: 'red', 
    0.5: 'purple'
}

# Add animated heatmap to map with custom gradient and radius
HeatMapWithTime(data_per_date, index=dates, auto_play=True, max_opacity=1, gradient=gradient, radius=20, blur=1).add_to(m)

# Save map to HTML
map_filename = 'animated_heatmap_chesapeake_yearly.html'
m.save(os.path.join(map_filename))

print(f"Map saved to {map_filename}")
