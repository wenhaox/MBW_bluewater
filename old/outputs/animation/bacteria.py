import folium
from folium import plugins
import json
from datetime import datetime

# Load your data
json_file_path = 'geojson/test.json'  # Update this path
with open(json_file_path, 'r') as file:
    bacteria_data = json.load(file)

# Prepare your data: You need to aggregate your data by month and convert it into GeoJSON format.
# This is a simplified example of what your GeoJSON might look like.
geojson_features = {
    "type": "FeatureCollection",
    "features": [
        # Example feature for one month - you would generate this based on your data
        {
            "type": "Feature",
            "properties": {
                "time": "2023-01-01",  # Use the first day of each month as the timestamp
            },
            "geometry": {
                "type": "Point",
                "coordinates": [-76.61, 39.26]  # Example coordinates
            }
        },
        # Add more features for each month
    ]
}

# Initialize the map
m = folium.Map(location=[39.26, -76.61], zoom_start=12)

# Add a Timestamped GeoJSON layer
time_layer = plugins.TimestampedGeoJson(
    geojson_features,
    period='P1M',  # Sets the period to one month
    add_last_point=True,
    auto_play=False,
    loop=False,
    max_speed=1,
    loop_button=True,
    date_options='YYYY/MM',
    time_slider_drag_update=True
)

m.add_child(time_layer)

# Save the map
m.save('bacteria_time_animation.html')
