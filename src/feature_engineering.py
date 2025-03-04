import pandas as pd

import pandas as pd

def calculate_future_returns(df: pd.DataFrame, future_window: int = 5) -> pd.DataFrame:
    """
    Calculates the percentage future return over a given time window.

    Parameters:
    df (pd.DataFrame): DataFrame containing a 'close' price column.
    future_window (int): Number of periods (minutes) ahead to calculate the return.

    Returns:
    pd.DataFrame: DataFrame with a new column 'future_return_Xmin' representing future return.
    """
    col_name = f"future_return_{future_window}min"
    
    # Future price after `future_window` periods
    future_price = df.groupby("symbol")["close"].shift(-future_window)
    
    # Calculate future return
    df[col_name] = (future_price - df["close"]) / df["close"]

    # Handle NaNs (last `future_window` rows will be NaN because they have no future price)
    df[col_name].fillna(0, inplace=True) 

    return df