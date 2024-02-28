import os
import folium
from folium.plugins import HeatMapWithTime

# Initialize map at Baltimore, MD.
m = folium.Map(location=[39.2904, -76.6122], zoom_start=13)

# Data points for each date, with latitude, longitude, and intensity.
data_per_date = [
    [[39.2904, -76.6122, 0.5], [39.2924, -76.6022, 0.8]],  # 01/01/2024
    [[39.2904, -76.6122, 0.7], [39.2924, -76.6022, 0.3]],  # 02/01/2024
    [[39.2844, -76.6202, 0.2], [39.2964, -76.6222, 0.9]],  # 03/01/2024
    [[39.2984, -76.6322, 0.4], [39.2844, -76.6202, 0.6]],  # 04/01/2024
]

# Dates for each data set.
dates = ["01/01/2024", "02/01/2024", "03/01/2024", "04/01/2024"]

# Add animated heatmap to map.
HeatMapWithTime(data_per_date, index=dates, auto_play=True, max_opacity=0.8).add_to(m)

# Save map to HTML.
m.save(os.path.join('animated_heatmap_baltimore_with_inline_dates.html'))
