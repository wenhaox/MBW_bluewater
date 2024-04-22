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

# Proceed with your filtering by date range after normalization
start_date = pd.to_datetime('2009-01-01')
end_date = pd.to_datetime('2030-12-01')
filtered_df = filtered_df[(filtered_df['collection_date'] >= start_date) & (filtered_df['collection_date'] <= end_date)]

# Transform the filtered data for HeatMapWithTime
data_per_date = []
dates = []

for date in np.sort(filtered_df['collection_date'].unique()):
    date = pd.to_datetime(date).to_pydatetime()
    day_data = filtered_df[filtered_df['collection_date'] == date]
    # Here we replace the original values with normalized values
    heat_data = day_data[['latitude', 'longitude', 'normalized_value']].values.tolist()
    data_per_date.append(heat_data)
    dates.append(date.strftime('%Y-%m-%d'))

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


HeatMapWithTime(data_per_date, index=dates, auto_play=True, max_opacity=0.8, gradient=gradient, radius=50, use_local_extrema=False).add_to(m)

# Save map to HTML
map_filename = 'animated_heatmap_baltimore_yearly.html'
m.save(map_filename)

print(f"Map saved to {map_filename}")