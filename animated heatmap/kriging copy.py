import pandas as pd
from pykrige.ok import OrdinaryKriging
import numpy as np

# Load the dataset with filled values
data_path = 'animated heatmap/processed data/bacteria_data_filled.csv'
data = pd.read_csv(data_path)

# Convert the 'collection_date' to datetime format for easier handling
data['collection_date'] = pd.to_datetime(data['collection_date'])

# Initialize an empty DataFrame to store kriging results for all dates
kriged_data_all_dates = pd.DataFrame()

for date in data['collection_date'].unique():
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

    # Calculate the minimum and maximum coordinates for the current date
    min_latitude = latitude.min()
    max_latitude = latitude.max()
    min_longitude = longitude.min()
    max_longitude = longitude.max()

    # Set up the grid using the calculated minimum and maximum coordinates
    lat_grid, lon_grid = np.mgrid[min_latitude:max_latitude:10j, 
                                  min_longitude:max_longitude:10j]

    try:
        # Attempt Ordinary Kriging with a specified variogram model
        OK = OrdinaryKriging(longitude, latitude, bacteria_levels, variogram_model='linear',
                             verbose=False, enable_plotting=False)
        # Predict bacteria levels on the grid
        z, ss = OK.execute('grid', lon_grid, lat_grid)
    except ValueError as e:
        print(f"Skipping date {date} due to error: {e}")
        continue  # Skip to the next date if kriging fails

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

# Save the kriged data for all dates to a CSV file
predicted_data_path = 'animated heatmap/processed data/predicted_kriged_bacteria_levels.csv'
kriged_data_all_dates.to_csv(predicted_data_path, index=False)

print(f'Predicted bacteria levels for all dates saved to {predicted_data_path}')
