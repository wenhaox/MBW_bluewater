import pandas as pd
import plotly.express as px

# Load CSV data
df = pd.read_csv('animated heatmap/processed data/combined_original_and_predicted_data.csv')

# Create 'collection_date' column
df['collection_date'] = pd.to_datetime(df[['year', 'month']].assign(DAY=1))

# Ensure 'collection_date' is in datetime format
df['collection_date'] = pd.to_datetime(df['collection_date'])

# Create a new column 'month_year' to store only the month and year part of 'collection_date'
df['month_year'] = df['collection_date'].dt.to_period('M')

# Group by 'month_year' and calculate the mean of 'Enterococcus Bacteria (MPN/100mL) - A2LA Lab'
monthly_average = df.groupby('month_year')['Enterococcus Bacteria (MPN/100mL) - A2LA Lab'].mean().reset_index()

# Convert 'month_year' back to datetime format for plotting
monthly_average['month_year'] = monthly_average['month_year'].dt.to_timestamp()

# Plotting with plotly
fig = px.line(monthly_average, x='month_year', y='Enterococcus Bacteria (MPN/100mL) - A2LA Lab',
              title='Monthly Average of Enterococcus Bacteria (MPN/100mL)',
              labels={'month_year': 'Month and Year', 'Enterococcus Bacteria (MPN/100mL) - A2LA Lab': 'Average Enterococcus Bacteria (MPN/100mL)'},
              markers=True)

# Hover data formatting
fig.update_traces(mode='markers+lines', hovertemplate='%{x|%B %Y}: %{y:.2f}')
fig.update_layout(xaxis_title='Month and Year', yaxis_title='Average Enterococcus Bacteria (MPN/100mL)',
                  xaxis=dict(tickformat="%b %Y"), hovermode='closest')

fig.show()
