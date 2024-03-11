import pandas as pd
import folium
from folium.plugins import HeatMapWithTime
import os
import numpy as np
from sklearn.preprocessing import MinMaxScaler

# Load CSV data
df = pd.read_csv('animated heatmap/processed data/predicted_kriged_bacteria_levels.csv')

# Ensure collection_date is a datetime type
df['collection_date'] = pd.to_datetime(df['collection_date'])

# Specify your start and end dates here
start_date = pd.to_datetime('2009-05-22')
end_date = pd.to_datetime('2013-07-03') 

# Filter the dataframe by date range
filtered_df = df[(df['collection_date'] >= start_date) & (df['collection_date'] <= end_date)]

# Normalize the 'predicted_bacteria_levels' within the filtered dataset
bacteria_levels = filtered_df['predicted_bacteria_levels'].values.reshape(-1, 1)
scaler = MinMaxScaler(feature_range=(0, 1))
normalized_bacteria_levels = scaler.fit_transform(bacteria_levels)
filtered_df['normalized_bacteria_levels'] = normalized_bacteria_levels.flatten()

# Transform the filtered data for HeatMapWithTime using normalized bacteria levels
data_per_date = []
dates = []

for date in np.sort(filtered_df['collection_date'].unique()):
    date = pd.to_datetime(date).to_pydatetime()
    day_data = filtered_df[filtered_df['collection_date'] == date]
    # Use 'normalized_bacteria_levels' instead of 'predicted_bacteria_levels'
    heat_data = day_data[['latitude', 'longitude', 'normalized_bacteria_levels']].values.tolist()
    data_per_date.append(heat_data)
    dates.append(date.strftime('%Y-%m-%d'))

# Initialize map at Baltimore, MD.
m = folium.Map(location=[39.2904, -76.6122], zoom_start=13)

# Custom gradient
gradient = {0.4: 'blue', 0.7: 'lime', 0.9: 'red'}

# Add animated heatmap to map with custom gradient and radius
HeatMapWithTime(data_per_date, index=dates, auto_play=True, max_opacity=0.9, gradient=gradient, radius=20, blur=1).add_to(m)

# Save map to HTML.
map_filename = 'animated_heatmap_baltimore_yearly.html'
m.save(os.path.join(map_filename))

print(f"Map saved to {map_filename}")
