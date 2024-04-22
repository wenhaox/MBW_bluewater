import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Load data and count unique stations
def load_data(filepath):
    data = pd.read_csv(filepath)
    unique_stations = data.drop_duplicates(subset=['latitude', 'longitude'])
    num_stations = unique_stations.shape[0]
    print(f"Total number of unique stations: {num_stations}")
    return data

# Calculate average bacteria levels per station
def average_per_station(data):
    return data.groupby(['latitude', 'longitude'])['Enterococcus Bacteria (MPN/100mL) - A2LA Lab'].agg(['mean', 'count']).sort_values(by='mean', ascending=False).reset_index()

# Calculate monthly average bacteria levels
def monthly_averages(data):
    return data.groupby('month')['Enterococcus Bacteria (MPN/100mL) - A2LA Lab'].mean()

# Calculate yearly average bacteria levels
def yearly_averages(data):
    return data.groupby('year')['Enterococcus Bacteria (MPN/100mL) - A2LA Lab'].mean()

# Plot top contaminated stations
def plot_top_contaminated_stations(stations):
    # Define a custom color scale from yellow to red
    yellow_to_red = ['rgb(255,255,0)', 'rgb(255,165,0)', 'rgb(255,0,0)']
    # Base map with all stations, less emphasized, in blue
    fig = go.Figure(go.Scattermapbox(
        lat=stations['latitude'],
        lon=stations['longitude'],
        mode='markers',
        marker=go.scattermapbox.Marker(
            size=8,  # Uniform size for all non-top-10 stations
            color='blue',  # Consistent color for non-highlighted points
            opacity=0.5
        ),
        hoverinfo='text',
        hovertext=stations['mean']
    ))
    # Add the top 10 contaminated stations with a color scale
    top_stations = stations.head(10)
    fig.add_trace(go.Scattermapbox(
        lat=top_stations['latitude'],
        lon=top_stations['longitude'],
        mode='markers',
        marker=go.scattermapbox.Marker(
            size=top_stations['mean']/stations['mean'].max() * 20 + 5,  # Scaled size
            color=top_stations['mean'],  # Color based on contamination level
            colorscale=yellow_to_red,  # Custom color scale
            cmin=stations['mean'].min(),  # Minimum of scale
            cmax=stations['mean'].max(),  # Maximum of scale
            opacity=0.8,
            showscale=True  # Show color scale
        ),
        hoverinfo='text',
        hovertext=top_stations['mean']
    ))
    # Adjust map style for better visibility
    fig.update_layout(
        mapbox_style="carto-positron",  # Clear and bright base map style
        mapbox_zoom=10,
        mapbox_center={"lat": stations['latitude'].mean(), "lon": stations['longitude'].mean()},
        margin={"r":0,"t":0,"l":0,"b":0},
        title="All Stations with Top 10 Contaminated Highlighted"
    )
    fig.show()

# Main function to run the analysis
def run_analysis(filepath):
    data = load_data(filepath)
    # Get average per station and print top 10 contaminated stations
    stations = average_per_station(data)
    print("Top 10 contaminated stations:")
    print(stations.head(10))
    # Plot top contaminated stations
    plot_top_contaminated_stations(stations)
    # Get and print monthly averages
    monthly_data = monthly_averages(data)
    print("\nMonthly average bacteria levels:")
    print(monthly_data)
    # Get and print yearly averages
    yearly_data = yearly_averages(data)
    print("\nYearly average bacteria levels:")
    print(yearly_data)

# Filepath to your data
filepath = 'animated heatmap/processed data/bacteria_data_filled.csv'
run_analysis(filepath)
