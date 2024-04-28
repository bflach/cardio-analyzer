import pandas as pd


def moving_average(data, window_size=30):
    """
    Calculate the moving average over an adjustable period of time for Sys, Dia, and Pulse data.

    Parameters:
    - data: Pandas DataFrame containing the dataset with 'Date', 'Sys', 'Dia', and 'Pulse' columns.
    - window_size: Integer, the size of the moving average window. Default is set to one month.

    Returns:
    - averaged_data: Pandas DataFrame with additional columns for the moving averages of Sys, Dia, and Pulse.
    """
    data['Date'] = pd.to_datetime(data['Date'])
    data.set_index('Date', inplace=True)

    # Calculate moving averages
    averaged_data = data[['Sys', 'Dia', 'Pulse']].rolling(window=window_size).mean()

    # Rename columns to indicate they represent moving averages
    averaged_data.rename(columns={'Sys': 'Sys_MA', 'Dia': 'Dia_MA', 'Pulse': 'Pulse_MA'}, inplace=True)

    # Combine original data with moving averages
    result_data = pd.concat([data, averaged_data], axis=1)

    return result_data


def moving_average_with_classification(data, window_size=30, bp_range=(90, 120, 80, 90)):
    """
    Calculate the moving average, minimum, and maximum values over an adjustable period of time for Sys, Dia, and Pulse data.
    Add background color to indicate the classification of the blood pressure range.

    Parameters:
    - data: Pandas DataFrame containing the dataset with 'Date', 'Sys', 'Dia', and 'Pulse' columns.
    - window_size: Integer, the size of the moving average window. Default is set to one month.
    - bp_range: Tuple, representing the blood pressure range classification (Sys_low, Sys_high, Dia_low, Dia_high).
                 Default values are set for a typical range.

    Returns:
    - result_data: Pandas DataFrame with additional columns for moving averages, min, max, and blood pressure range classification.
    """
    data['Date'] = pd.to_datetime(data['Date'])
    data.set_index('Date', inplace=True)

    # Calculate moving averages, min, and max
    averaged_data = data[['Sys', 'Dia', 'Pulse']].rolling(window=window_size).mean()
    min_values = data[['Sys', 'Dia', 'Pulse']].rolling(window=window_size).min()
    max_values = data[['Sys', 'Dia', 'Pulse']].rolling(window=window_size).max()

    # Rename columns
    averaged_data.rename(columns={'Sys': 'Sys_MA', 'Dia': 'Dia_MA', 'Pulse': 'Pulse_MA'}, inplace=True)
    min_values.rename(columns={'Sys': 'Sys_Min', 'Dia': 'Dia_Min', 'Pulse': 'Pulse_Min'}, inplace=True)
    max_values.rename(columns={'Sys': 'Sys_Max', 'Dia': 'Dia_Max', 'Pulse': 'Pulse_Max'}, inplace=True)

    # Combine original data with moving averages, min, and max
    result_data = pd.concat([data, averaged_data, min_values, max_values], axis=1)

    # Blood Pressure Range Classification
    sys_low, sys_high, dia_low, dia_high = bp_range

    # Classify blood pressure based on the range
    result_data['BP_Classification'] = 'Normal'
    result_data.loc[
        (result_data['Sys_MA'] >= sys_high) | (result_data['Dia_MA'] >= dia_high), 'BP_Classification'] = 'Hypertension'
    result_data.loc[
        (result_data['Sys_MA'] < sys_low) | (result_data['Dia_MA'] < dia_low), 'BP_Classification'] = 'Hypotension'

    # Background Color based on Classification
    def classify_color(bp_classification):
        if bp_classification == 'Normal':
            return 'background-color: #aaffaa;'  # Light green
        elif bp_classification == 'Hypertension':
            return 'background-color: #ffaaaa;'  # Light red
        elif bp_classification == 'Hypotension':
            return 'background-color: #aaaaff;'  # Light blue
        else:
            return ''

    return result_data
