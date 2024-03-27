import pandas as pd
import folium
from folium.plugins import HeatMapWithTime
import os
import numpy as np
from sklearn.preprocessing import MinMaxScaler
# https://pypi.org/project/global-land-mask/
# Load CSV data
df = pd.read_csv('animated heatmap/processed data/combined_original_and_predicted_data.csv')

# Create 'collection_date' column by combining 'year' and 'month', assuming the day as the first of each month for simplicity
df['collection_date'] = pd.to_datetime(df[['year', 'month']].assign(DAY=1))

# Normalize the 'Enterococcus Bacteria (MPN/100mL) - A2LA Lab' within the entire dataset
# First, handle missing data appropriately. Here, simply filling with zeros or some form of imputation if better for your analysis
df['Enterococcus Bacteria (MPN/100mL) - A2LA Lab'] = df['Enterococcus Bacteria (MPN/100mL) - A2LA Lab'].fillna(0)

scaler = MinMaxScaler(feature_range=(0, 1))
df['normalized_value'] = scaler.fit_transform(df[['Enterococcus Bacteria (MPN/100mL) - A2LA Lab']])

# Filter the dataframe by date range after normalization to include all points in normalization
start_date = pd.to_datetime('2009-01-01')
end_date = pd.to_datetime('2030-12-01') 
filtered_df = df[(df['collection_date'] >= start_date) & (df['collection_date'] <= end_date)]

# Transform the filtered data for HeatMapWithTime
data_per_date = []
dates = []

for date in np.sort(filtered_df['collection_date'].unique()):
    date = pd.to_datetime(date).to_pydatetime()
    day_data = filtered_df[filtered_df['collection_date'] == date]
    heat_data = day_data[['latitude', 'longitude', 'normalized_value']].values.tolist()
    data_per_date.append(heat_data)
    dates.append(date.strftime('%Y-%m-%d'))

# Initialize and configure the heatmap
m = folium.Map(location=[39.2904, -76.6122], zoom_start=9)
gradient = {
    0.1: 'blue', 
    0.2: 'lime', 
    0.3: 'yellow', 
    0.5: 'orange', 
    0.7: 'red', 
    0.95: 'purple'
}
HeatMapWithTime(data_per_date, index=dates, auto_play=True, max_opacity=0.8, gradient=gradient, radius=20, use_local_extrema=True).add_to(m)

# Save map to HTML.
map_filename = 'animated_heatmap_baltimore_yearly.html'
m.save(map_filename)

print(f"Map saved to {map_filename}")
