import pandas as pd
import folium
from folium.plugins import HeatMapWithTime
import numpy as np
from sklearn.preprocessing import MinMaxScaler
import global_land_mask as glm

# Load CSV data
df = pd.read_csv('animated heatmap/processed data/combined_original_and_predicted_data.csv')

# Create 'collection_date' column
df['collection_date'] = pd.to_datetime(df[['year', 'month', 'day_of_year']])

# Normalize the 'Enterococcus Bacteria (MPN/100mL) - A2LA Lab' column
df['Enterococcus Bacteria (MPN/100mL) - A2LA Lab'] = df['Enterococcus Bacteria (MPN/100mL) - A2LA Lab'].fillna(0)
scaler = MinMaxScaler(feature_range=(0, 1))
df['normalized_value'] = scaler.fit_transform(df[['Enterococcus Bacteria (MPN/100mL) - A2LA Lab']])

# Identify points to keep
df['keep_point'] = df.apply(lambda row: True if row['data_type'] == 'original' else not glm.is_land(row['latitude'], row['longitude']), axis=1)
filtered_df = df[df['keep_point']]

# Proceed with your filtering by date range after normalization
start_date = pd.to_datetime('2009-01-01')
end_date = pd.to_datetime('2030-12-31')
filtered_df = filtered_df[(filtered_df['collection_date'] >= start_date) & (filtered_df['collection_date'] <= end_date)]

# Transform the filtered data for HeatMapWithTime
data_per_date = []
dates = []

for date in pd.date_range(start='2009-01-01', end='2030-12-31', freq='D'):
    date = pd.to_datetime(date).to_pydatetime()
    day_data = filtered_df[filtered_df['collection_date'] == date]
    # Here we replace the original values with normalized values
    heat_data = day_data[['latitude', 'longitude', 'Enterococcus Bacteria (MPN/100mL) - A2LA Lab']].values.tolist()
    data_per_date.append(heat_data)
    dates.append(date.strftime('%Y-%m-%d'))

# Initialize and configure the heatmap
m = folium.Map(location=[39.2904, -76.6122], zoom_start=12, zoom_control=False)

gradient = {
    0.0: 'blue', 
    0.2: 'cyan', 
    0.4: 'lime', 
    0.6: 'yellow', 
    0.8: 'orange', 
    0.9: 'red', 
    1.0: 'purple'
}

HeatMapWithTime(data_per_date, index=dates, auto_play=True, max_opacity=0.7, gradient=gradient, radius=50, use_local_extrema=True).add_to(m)

# Save map to HTML
map_filename = 'animated_heatmap_baltimore_yearly.html'
m.save(map_filename)

print(f"Map saved to {map_filename}")
