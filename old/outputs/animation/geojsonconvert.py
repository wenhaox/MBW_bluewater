# The provided code snippet needs adjustment to correctly load the JSON data into a DataFrame,
# and then convert the DataFrame to GeoJSON format for use with Folium's HeatMap.
import pandas as pd
import json
from datetime import datetime

# Load the monthly averages data from the correct JSON file path
json_file_path = 'data/monthly_avg_bacteria.json'  # Corrected path to use the previously saved monthly averages data
with open(json_file_path, 'r') as file:
    monthly_averages_data = json.load(file)

# Convert the loaded data into a pandas DataFrame
df_monthly_averages = pd.DataFrame(monthly_averages_data)

# Ensure 'year_month' is in datetime format
df_monthly_averages['year_month'] = pd.to_datetime(df_monthly_averages['year_month'])

def df_to_geojson(df, properties, lat='latitude', lon='longitude'):
    geojson = {'type': 'FeatureCollection', 'features': []}
    for _, row in df.iterrows():
        feature = {
            'type': 'Feature',
            'properties': {},
            'geometry': {
                'type': 'Point',
                'coordinates': [],
            },
        }
        feature['geometry']['coordinates'] = [row[lon], row[lat]]
        for prop in properties:
            # Ensure datetime is converted to string properly
            if isinstance(row[prop], datetime):
                feature['properties'][prop] = row[prop].isoformat()
            else:
                feature['properties'][prop] = row[prop]
        geojson['features'].append(feature)
    return geojson

# Specify properties to include in the GeoJSON (adjusting property names as necessary)
properties = ['year_month', 'Enterococcus Bacteria (MPN/100mL) - A2LA Lab']

# Convert DataFrame to GeoJSON
geojson_data = df_to_geojson(df_monthly_averages, properties)

# Display the first feature to ensure it's structured correctly
geojson_data['features'][:1]