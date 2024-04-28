"""
This is based on the following conversation:
https://chat.openai.com/c/1de07854-ea9d-4a8f-845d-264ba42880f4
"""
# Load data from CSV file
csv_file_path = '2024-01-08_blood-pressure-data.csv'  # Replace with the path to your CSV file

import pandas as pd
import matplotlib.pyplot as plt

from utilities_cardio import moving_average
from utilities_cardio import moving_average_with_classification

# Load data from CSV file
df = pd.read_csv(csv_file_path)

# Time Series Analysis
df['Date'] = pd.to_datetime(df['Date'])
df.set_index('Date', inplace=True)

# Long-Term Changes - Regression Analysis
from sklearn.linear_model import LinearRegression


def regression_analysis(data, target_col, feature_col):
    model = LinearRegression()
    model.fit(data[feature_col].values.reshape(-1, 1), data[target_col])
    slope = model.coef_[0]
    intercept = model.intercept_
    return slope, intercept


df["Date"] = df.index
systolic_slope, systolic_intercept = regression_analysis(df, 'Sys', 'Date')
diastolic_slope, diastolic_intercept = regression_analysis(df, 'Dia', 'Date')
pulse_slope, pulse_intercept = regression_analysis(df, 'Pulse', 'Date')

print(f"\nSystolic Trend: Slope={systolic_slope}, Intercept={systolic_intercept}")
print(f"Diaselectablestolic Trend: Slope={diastolic_slope}, Intercept={diastolic_intercept}")
print(f"Pulse Trend: Slope={pulse_slope}, Intercept={pulse_intercept}")

# Health Insights - Pulse Pressure Calculation
df['PulsePressure'] = df['Sys'] - df['Dia']
# Histograms
df.hist(bins=20, figsize=(12, 10))
plt.suptitle("Histograms of Blood Pressure and Pulse Measurements")
plt.savefig("hist.pdf")

# Additional Analyses...
# (You can add more analyses based on your specific requirements)

result_df = moving_average_with_classification(df)

# Display the resulting DataFrame with styling for background color
result_df.to_excel('result_data_with_classification.xlsx', engine='openpyxl', index=False)  # Save to Excel
