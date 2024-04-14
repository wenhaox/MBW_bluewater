import pandas as pd
from sklearn.linear_model import LinearRegression
import numpy as np

# Load the data
file_path = '/Users/peter/Desktop/MBW_Bluewater/data/bacteria_data.csv'  # Update file path to point to the uploaded dataset
data = pd.read_csv(file_path)
data = data.dropna(subset=['Enterococcus Bacteria (MPN/100mL) - A2LA Lab'])

# Convert 'collection_date' to datetime and extract 'day_of_year'
data['collection_date'] = pd.to_datetime(data['collection_date'])
data['day_of_year'] = data['collection_date'].dt.dayofyear

# Determine the full date range in the dataset
min_date = data['collection_date'].min()
max_date = data['collection_date'].max()
all_dates = pd.date_range(start=min_date, end=max_date)

# Create a grid of all latitude-longitude pairs and dates
unique_lat_lon = data[['latitude', 'longitude']].drop_duplicates()
date_grid = pd.DataFrame(all_dates, columns=['collection_date'])
date_grid['key'] = 1
unique_lat_lon['key'] = 1
complete_grid = pd.merge(unique_lat_lon, date_grid, on='key').drop('key', axis=1)
complete_grid['day_of_year'] = complete_grid['collection_date'].dt.dayofyear

# Merge the complete grid with the original dataset to ensure all combinations are present
merged_data = pd.merge(complete_grid, data, on=['latitude', 'longitude', 'collection_date', 'day_of_year'], how='left')

filled_data = pd.DataFrame()

for (lat, lon), group in merged_data.groupby(['latitude', 'longitude']):
    # Sort data by day_of_year for proper interpolation
    group = group.sort_values(by='day_of_year')
    # Perform linear interpolation
    group['Enterococcus Bacteria (MPN/100mL) - A2LA Lab'] = group['Enterococcus Bacteria (MPN/100mL) - A2LA Lab'].interpolate()

    filled_data = pd.concat([filled_data, group], ignore_index=True)

# Ensure the final dataset is sorted by collection_date
filled_data = filled_data.sort_values(by=['collection_date', 'latitude', 'longitude'])

# Calculate monthly averages
filled_data['year'] = filled_data['collection_date'].dt.year
filled_data['month'] = filled_data['collection_date'].dt.month
monthly_avg = filled_data.groupby(['latitude', 'longitude', 'year', 'month'], as_index=False).mean(numeric_only=True)
monthly_avg.drop(columns=['day_of_year'], inplace=True)  # Drop 'day_of_year' as it's no longer relevant
monthly_avg = monthly_avg.dropna(subset=['Enterococcus Bacteria (MPN/100mL) - A2LA Lab'])

# Save the regression-filled dataset
filled_data_path = 'animated heatmap/processed data/bacteria_data_filled.csv'  # Update the path as needed
filled_data.to_csv(filled_data_path, index=False)

# Save the monthly averages to a CSV file
monthly_avg_path = 'animated heatmap/processed data/monthly_averages.csv'  # Update the path as needed
monthly_avg.to_csv(monthly_avg_path, index=False)

print(f'Dataset with filled values saved to {filled_data_path}')
print(f'Monthly averages saved to {monthly_avg_path}')
