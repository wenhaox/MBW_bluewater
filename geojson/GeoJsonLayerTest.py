import pydeck as pdk
import json

# Use the local path to your GeoJSON file
DATA_URL = "output_geojson_hexagons.json"  # Make sure this path is correct

# Debug step: Load and print a portion of the GeoJSON file to ensure it's read correctly
with open(DATA_URL, 'r') as f:
    geojson_data = json.load(f)
    print("Loaded GeoJSON data:")
    print(json.dumps(geojson_data["features"][0], indent=2))  # Print the first feature

INITIAL_VIEW_STATE = pdk.ViewState(
    latitude= 39.253541,  # Adjust based on the geographic focus of your data
    longitude= -76.574837,  # Adjust based on the geographic focus of your data
    zoom=12,
    max_zoom=16,
    pitch=45,
    bearing=0
)

geojson = pdk.Layer(
    "GeoJsonLayer",
    geojson_data,  # Use the loaded GeoJSON data directly
    opacity=0.8,
    stroked=False,
    filled=True,
    extruded=True,
    wireframe=True,
    get_elevation="properties['Total Water Depth (ft)'] * 100",
    get_fill_color="[255, 255, properties['Total Water Depth (ft)'] / 30  * 255]",
    get_line_color=[255, 255, 255],
)

r = pdk.Deck(layers=[geojson], initial_view_state=INITIAL_VIEW_STATE)

r.to_html("geojson_layer.html")
