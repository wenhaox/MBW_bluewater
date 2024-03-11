import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.impute import SimpleImputer
import numpy as np

# Load the data
file_path = 'data/bacteria_data.csv'  # Update the file path accordingly
data = pd.read_csv(file_path)

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
    # Your X and y definitions
    X = group[['day_of_year']]
    y = group['Enterococcus Bacteria (MPN/100mL) - A2LA Lab']  # Assuming this is the target column

    # Ensure there are actual data points to train on
    if y.notnull().sum() > 0:
        # Splitting into train and prediction subsets based on y being null or not
        X_train = X[y.notnull()]
        y_train = y[y.notnull()]
        X_predict = X[y.isnull()]

        # Check if we have at least two points to train on
        if len(X_train) > 1:
            # Training the model
            model = LinearRegression()
            model.fit(X_train, y_train)

            # Making predictions only if there are missing y values
            if not X_predict.empty:
                predictions = model.predict(X_predict)

                # Assigning predictions to the original dataset
                group.loc[y.isnull(), 'Enterococcus Bacteria (MPN/100mL) - A2LA Lab'] = predictions

    # Append corrected group to filled_data
    filled_data = pd.concat([filled_data, group])

# Before saving, ensure the final dataset is sorted by collection_date
filled_data = filled_data.sort_values(by=['collection_date', 'latitude', 'longitude'])

filled_data_path = 'animated heatmap/processed data/bacteria_data_filled.csv'
filled_data.to_csv(filled_data_path, index=False)

print(f'Dataset with filled values saved to {filled_data_path}')
