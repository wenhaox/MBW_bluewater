import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# Load CSV data
df = pd.read_csv('animated heatmap/processed data/combined_original_and_predicted_data.csv')

# Create 'collection_date' column
df['collection_date'] = pd.to_datetime(df[['year', 'month']].assign(DAY=1))

# Normalize the 'Enterococcus Bacteria (MPN/100mL) - A2LA Lab' column
df['Enterococcus Bacteria (MPN/100mL) - A2LA Lab'] = df['Enterococcus Bacteria (MPN/100mL) - A2LA Lab'].fillna(0)
scaler = MinMaxScaler(feature_range=(0, 1))
df['normalized_value'] = df['Enterococcus Bacteria (MPN/100mL) - A2LA Lab'].rank(pct=True)

# Select data for a specific date
specific_date = pd.to_datetime('2009-05-01')
day_data = df[df['collection_date'] == specific_date]

# Round latitude and longitude to 2 decimal places
day_data['longitude'] = day_data['longitude'].round(2)
day_data['latitude'] = day_data['latitude'].round(2)

# Create a 3D scatter plot
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
sc = ax.scatter(day_data['longitude'], day_data['latitude'], day_data['normalized_value'], c=day_data['normalized_value'], cmap='viridis')

# Add color bar and labels
plt.colorbar(sc)
ax.set_xlabel('Longitude')
ax.set_ylabel('Latitude')
ax.set_zlabel('Normalized Value')

# Show plot
plt.show()
