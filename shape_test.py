import pandas as pd
import json
import math

# Load the dataset
file_path = 'data/BWB_AWQMP_Data_2009-2022_test.csv'  # Update this with the correct path to your CSV file
data = pd.read_csv(file_path)

def create_hexagon_polygon(lat, lon, size=0.002):
    """Generates a hexagon polygon around a point.
    The size parameter determines the 'radius' of the hexagon."""
    hexagon = []
    lon_adj = size / math.cos(math.radians(lat))
    for i in range(6):
        angle_deg = 60 * i
        angle_rad = math.pi / 180 * angle_deg
        hexagon.append([lon + lon_adj * math.cos(angle_rad), lat + size * math.sin(angle_rad)])
    return hexagon

geojson = {
    "type": "FeatureCollection",
    "features": []
}

for index, row in data.iterrows():
    polygon = create_hexagon_polygon(row['latitude'], row['longitude'])
    feature = {
        "type": "Feature",
        "geometry": {
            "type": "Polygon",
            "coordinates": [polygon]
        },
        "properties": {
            "station_id": row['station_id'],
            "collection_date": row['collection_date'],
            "Total Water Depth (ft)": row['Total Water Depth (ft)'],
            "Nitrate/Nitrite (mg/L)": row['Nitrate/Nitrite (mg/L)'],
            "Total Nitrogen (mg/L)": row['Total Nitrogen (mg/L)'],
            "Total Phosphorus (mg/L)": row['Total Phosphorus (mg/L)'],
            "Total Kjeldahl Nitrogen (mg/L)": row['Total Kjeldahl Nitrogen (mg/L)'],
            "Chlorophyll (µg/L)": row['Chlorophyll (µg/L)']
        }
    }
    geojson["features"].append(feature)

# Saving the generated GeoJSON to a file
with open('output_geojson_hexagons.json', 'w') as f:
    json.dump(geojson, f, indent=2)
