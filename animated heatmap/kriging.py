import pandas as pd
from pykrige.ok import OrdinaryKriging
import numpy as np

# Load the dataset with filled values
data_path = '/Users/peter/Desktop/MBW_Bluewater/animated heatmap/processed data/bacteria_data_filled.csv'  # Update this path to your actual data file location
data = pd.read_csv(data_path)

# Convert the 'collection_date' to datetime format for easier handling
data['collection_date'] = pd.to_datetime(data['collection_date'])

# Pre-calculate global min and max coordinates to ensure consistency
global_min_latitude = data['latitude'].min()
global_max_latitude = data['latitude'].max()
global_min_longitude = data['longitude'].min()
global_max_longitude = data['longitude'].max()

# Initialize an empty DataFrame to store kriging results for all dates
kriged_data_all_dates = pd.DataFrame()

for date in data['collection_date'].unique():
    try:
        # Filter data for the current date
        data_date = data[data['collection_date'] == date]

        # Ensure data quality and check for sufficient variability
        if data_date[['latitude', 'longitude', 'Enterococcus Bacteria (MPN/100mL) - A2LA Lab']].dropna().empty or \
                len(data_date['latitude'].unique()) <= 1 or len(data_date['longitude'].unique()) <= 1:
            print(f"Skipping date {date} due to insufficient data")
            continue  # Skip dates with insufficient data

        # Extract spatial coordinates and bacteria levels for the current date
        latitude = data_date['latitude'].values
        longitude = data_date['longitude'].values
        bacteria_levels = data_date['Enterococcus Bacteria (MPN/100mL) - A2LA Lab'].values

        if len(latitude) == 0 or len(longitude) == 0 or len(bacteria_levels) == 0:
            raise ValueError("One of the arrays is empty or not properly formatted.")

        # Use global coordinates to set up the grid
        lat_grid, lon_grid = np.mgrid[global_min_latitude:global_max_latitude:100j, 
                                      global_min_longitude:global_max_longitude:100j]

        # Attempt Ordinary Kriging with a specified variogram model
        OK = OrdinaryKriging(longitude, latitude, bacteria_levels, variogram_model='gaussian',
                             verbose=True, enable_plotting=False)
        # Predict bacteria levels on the grid
        z, ss = OK.execute('grid', lon_grid, lat_grid)

        # Flatten the grid matrices and the prediction matrix for saving
        lon_pred, lat_pred = np.meshgrid(lon_grid, lat_grid)
        lat_pred = lat_pred.ravel()
        lon_pred = lon_pred.ravel()
        z_pred = z.ravel()

        # Create a DataFrame from the predicted values and their coordinates for the current date
        predicted_data_date = pd.DataFrame({
            'collection_date': pd.to_datetime([date] * len(lat_pred)),
            'latitude': lat_pred,
            'longitude': lon_pred,
            'predicted_bacteria_levels': z_pred
        })

        # Append the results for the current date to the overall DataFrame
        kriged_data_all_dates = pd.concat([kriged_data_all_dates, predicted_data_date], ignore_index=True)

    except Exception as e:
        print(f"Error on date {date}: {e}")
        continue

# Save the kriged data for all dates to a CSV file
predicted_data_path = 'animated heatmap/processed data/predicted_kriged_bacteria_levels.csv'  # Update this path to where you want to save the file
kriged_data_all_dates.to_csv(predicted_data_path, index=False)

print(f'Predicted bacteria levels for all dates saved to {predicted_data_path}')
