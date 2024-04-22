import pandas as pd
import plotly.express as px

# Load CSV data
df = pd.read_csv('animated heatmap/processed data/combined_original_and_predicted_data.csv')

# Create 'collection_date' column
df['collection_date'] = pd.to_datetime(df[['year', 'month']].assign(DAY=1))

# Ensure 'collection_date' is in datetime format
df['collection_date'] = pd.to_datetime(df['collection_date'])

df['month_year'] = pd.to_datetime(df[['year', 'month']].assign(DAY=1))

# Group by 'month_year' and calculate the mean, handling non-numeric data properly
monthly_average = df.groupby(df['month_year'].dt.to_period('M')).mean(numeric_only=True).reset_index()
monthly_average['month_year'] = monthly_average['month_year'].dt.to_timestamp()

# Identify August data points
monthly_average['is_august'] = monthly_average['month_year'].dt.month == 8

# Plotting
fig = px.line(monthly_average, x='month_year', y='Enterococcus Bacteria (MPN/100mL) - A2LA Lab', title='Monthly Average of Enterococcus Bacteria (MPN/100mL)',
              markers=True, color_discrete_sequence=["blue"])  # Single line color

# Add custom markers for August
august_points = monthly_average[monthly_average['is_august']]
if not august_points.empty:
    fig.add_scatter(x=august_points['month_year'], y=august_points['Enterococcus Bacteria (MPN/100mL) - A2LA Lab'], mode='markers', marker=dict(color='red', size=10))

fig.update_layout(xaxis_title='Month and Year', yaxis_title='Average Enterococcus Bacteria (MPN/100mL)',
                  xaxis=dict(tickformat="%b %Y"), hovermode='closest',
                  title_font_size=24, font_family="Arial, sans-serif",
                  showlegend=False)  # Disable legend

fig.show()
