import pandas as pd
import numpy as np
from pykrige.ok import OrdinaryKriging

print("Starting script...")

# Load the data
data_path = 'animated heatmap/processed data/monthly_averages.csv'
print("Loading data...")
df = pd.read_csv(data_path)

# Prepare an empty DataFrame for storing predicted values
predicted_data_all = pd.DataFrame()

# Loop through each unique year-month combination
for (year, month), group in df.groupby(['year', 'month']):
    coordinates = group[['latitude', 'longitude']].values
    values = group['Enterococcus Bacteria (MPN/100mL) - A2LA Lab'].values

    # Setup Ordinary Kriging
    ok = OrdinaryKriging(
        coordinates[:, 0], coordinates[:, 1], values,
        variogram_model='gaussian',
        verbose=False,
        enable_plotting=False
    )

    # Define the grid points where predictions are needed
    grid_x = np.linspace(coordinates[:, 0].min(), coordinates[:, 0].max(), num=20)
    grid_y = np.linspace(coordinates[:, 1].min(), coordinates[:, 1].max(), num=20)
    grid_x, grid_y = np.meshgrid(grid_x, grid_y)

    # Predict values on the defined grid
    predicted_values = ok.execute('points', grid_x.flatten(), grid_y.flatten())[0].data

    # Create a DataFrame for the predicted data of the current group
    predicted_data = pd.DataFrame({
        'year': year,
        'month': month,
        'latitude': grid_x.flatten(),
        'longitude': grid_y.flatten(),
        'Enterococcus Bacteria (MPN/100mL) - A2LA Lab': predicted_values,
        'data_type': 'predicted'
    })

    # Append the current group's predictions to the overall DataFrame
    predicted_data_all = pd.concat([predicted_data_all, predicted_data])

# Sort the predicted data by year and month
predicted_data_all.sort_values(by=['year', 'month'], inplace=True)

# Save the predicted data to CSV
predicted_data_path = 'animated heatmap/processed data/predicted_data_only.csv'
predicted_data_all.to_csv(predicted_data_path, index=False)

print(f"Predicted data saved to {predicted_data_path}")
print("Script completed.")
