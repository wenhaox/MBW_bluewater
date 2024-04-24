import pandas as pd
import folium
from folium.plugins import HeatMapWithTime
import numpy as np
from sklearn.preprocessing import MinMaxScaler
import global_land_mask as glm

# Load CSV data
df = pd.read_csv('animated heatmap/processed data/combined_original_and_predicted_data.csv')

# Create 'collection_date' column
df['collection_date'] = pd.to_datetime(df[['year', 'month']].assign(DAY=1))

# Normalize the 'Enterococcus Bacteria (MPN/100mL) - A2LA Lab' column
df['Enterococcus Bacteria (MPN/100mL) - A2LA Lab'] = df['Enterococcus Bacteria (MPN/100mL) - A2LA Lab'].fillna(0)
scaler = MinMaxScaler(feature_range=(0, 1))
df['normalized_value'] = df['Enterococcus Bacteria (MPN/100mL) - A2LA Lab'].rank(pct=True)

# Identify points to keep
df['keep_point'] = df.apply(lambda row: True if row['data_type'] == 'original' else not glm.is_land(row['latitude'], row['longitude']), axis=1)
filtered_df = df[df['keep_point']]

# Group by month and compute average
monthly_avg = filtered_df.groupby([filtered_df['collection_date'].dt.month, 'latitude', 'longitude']).mean().reset_index()

# Transform the filtered data for HeatMapWithTime
data_per_month = []
months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']

for month in range(1, 13):
    month_data = monthly_avg[monthly_avg['collection_date'] == month]
    # Convert to list format suitable for the heatmap
    heat_data = month_data[['latitude', 'longitude', 'normalized_value']].values.tolist()
    data_per_month.append(heat_data)

# Initialize and configure the heatmap
m = folium.Map(location=[39.2904, -76.6122], zoom_start=12, zoom_control=False)

gradient = {
    0.3: '#3366cc', 
    0.7: '#33cccc',  
    0.85: '#ffff66', 
    0.9: '#ff9933',  
    0.97: '#ff5050',  
    0.99: '#cc33ff'   
}

HeatMapWithTime(data_per_month, index=months, auto_play=True, max_opacity=0.8, gradient=gradient, radius=35, use_local_extrema=False).add_to(m)

# Save map to HTML
map_filename = 'animated_heatmap_baltimore_average_year.html'
m.save(map_filename)

print(f"Map saved to {map_filename}")
