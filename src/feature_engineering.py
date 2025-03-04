import pandas as pd
from config.config import MA_WINDOWS, EMA_WINDOWS, MOMENTUM_PERIODS, VOLATILITY_WINDOWS, VOLUME_WINDOWS


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
    df[col_name] = df[col_name].fillna(0) 

    return df


def calculate_features(
    df,
    ma_windows=MA_WINDOWS,
    ema_windows=EMA_WINDOWS,
    momentum_periods=MOMENTUM_PERIODS,
    volatility_windows=VOLATILITY_WINDOWS,
    volume_windows=VOLUME_WINDOWS
):
    """Optimized batch feature engineering for all technical indicators."""
    df = df.sort_values(by=["symbol", "timestamp"])

    # Group by symbol for performance optimization
    grouped = df.groupby("symbol")

    # Apply moving averages (SMA)
    for window in ma_windows:
        df[f"sma_{window}"] = grouped["close"].transform(lambda x: x.rolling(window=window, min_periods=1).mean())

    # Apply exponential moving averages (EMA)
    for window in ema_windows:
        df[f"ema_{window}"] = grouped["close"].transform(lambda x: x.ewm(span=window, adjust=False).mean())

    # Apply momentum and rate of change (RoC)
    for period in momentum_periods:
        df[f"price_momentum_{period}"] = grouped["close"].diff(periods=period)
        df[f"roc_{period}"] = grouped["close"].pct_change(periods=period)

    # Apply rolling volatility (standard deviation)
    for window in volatility_windows:
        df[f"volatility_{window}"] = grouped["close"].transform(lambda x: x.rolling(window=window, min_periods=1).std())

    # Apply volume features (rolling mean + percentage change)
    for window in volume_windows:
        df[f"volume_rolling_mean_{window}"] = grouped["volume"].transform(lambda x: x.rolling(window=window, min_periods=1).mean())

    df["volume_change_5"] = grouped["volume"].pct_change(periods=5)

    return df