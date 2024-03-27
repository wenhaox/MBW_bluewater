import pandas as pd
import numpy as np
from pykrige.ok import OrdinaryKriging

print("Starting script...")

# Load the data
data_path = 'animated heatmap/processed data/monthly_averages.csv'
print("Loading data...")
df = pd.read_csv(data_path)

# Mark original data points as 'original'
df['data_type'] = 'original'

# Prepare an empty DataFrame for storing predicted values
predicted_data_all = pd.DataFrame()

# Loop through each unique year-month combination
for (year, month), group in df.groupby(['year', 'month']):
    coordinates = group[['latitude', 'longitude']].values
    values = group['Enterococcus Bacteria (MPN/100mL) - A2LA Lab'].values

    # Setup Ordinary Kriging
    ok = OrdinaryKriging(
        coordinates[:, 0], coordinates[:, 1], values,
        variogram_model='spherical',
        verbose=False,
        enable_plotting=False
    )

    # Define the grid points where predictions are needed
    grid_x = np.linspace(coordinates[:, 0].min(), coordinates[:, 0].max(), num=30)
    grid_y = np.linspace(coordinates[:, 1].min(), coordinates[:, 1].max(), num=30)
    grid_x, grid_y = np.meshgrid(grid_x, grid_y)

    # Predict values on the defined grid
    predicted_values = ok.execute('points', grid_x.flatten(), grid_y.flatten())[0].data

    # Create a DataFrame for the predicted data of the current group
    predicted_data = pd.DataFrame({
        'year': year,
        'month': month,
        'latitude': grid_x.flatten(),
        'longitude': grid_y.flatten(),
        'Enterococcus Bacteria (MPN/100mL) - A2LA Lab': predicted_values,  # Use the same column name for consistency
        'data_type': 'predicted'
    })

    # Append the current group's predictions to the overall DataFrame
    predicted_data_all = pd.concat([predicted_data_all, predicted_data])

combined_data = pd.concat([df, predicted_data_all])

# Sort the combined data by year and month
combined_data.sort_values(by=['year', 'month'], inplace=True)

# Save the combined data to CSV
combined_data_path = 'animated heatmap/processed data/combined_original_and_predicted_data.csv'
combined_data.to_csv(combined_data_path, index=False)

print(f"Combined original and predicted data saved to {combined_data_path}")
print("Script completed.")
