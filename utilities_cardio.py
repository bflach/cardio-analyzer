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
