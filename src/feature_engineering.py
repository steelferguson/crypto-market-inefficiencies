import pandas as pd
from config.config import (
  FUTURE_WINDOWS, TARGET_THRESHOLDS,
  MA_WINDOWS, EMA_WINDOWS, MOMENTUM_PERIODS, VOLATILITY_WINDOWS, VOLUME_WINDOWS, 
  RSI_WINDOWS, BOLLINGER_WINDOWS, MACD_WINDOWS
) 


def calculate_future_returns(df, future_windows=FUTURE_WINDOWS, thresholds=TARGET_THRESHOLDS):
    """Calculate future returns for regression and classify price movements at multiple thresholds."""
    
    df = df.sort_values(by=["symbol", "timestamp"])
    grouped = df.groupby("symbol")

    for window in future_windows:
        # Regression Target: Future % Return
        col_name = f"future_return_{window}min"
        df[col_name] = grouped["close"].shift(-window) / df["close"] - 1  # % change

        # Classification Targets: Multiple thresholds
        for threshold in thresholds:
            threshold_str = str(int(threshold * 100))  # Convert 0.05 → '5'
            df[f"increase_{threshold_str}pct_{window}min"] = (df[col_name] >= threshold).astype(int)  # Increase ≥ X%
            df[f"decrease_{threshold_str}pct_{window}min"] = (df[col_name] <= -threshold).astype(int)  # Decrease ≤ -X%

    return df


def calculate_features(
    df,
    ma_windows=MA_WINDOWS,
    ema_windows=EMA_WINDOWS,
    momentum_periods=MOMENTUM_PERIODS,
    volatility_windows=VOLATILITY_WINDOWS,
    volume_windows=VOLUME_WINDOWS,
    rsi_windows=RSI_WINDOWS,
    bollinger_windows=BOLLINGER_WINDOWS,
    macd_windows=MACD_WINDOWS,
):
    """Computes various technical indicators efficiently using grouped transformations."""
    df = df.sort_values(by=["symbol", "timestamp"])
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

    # Apply RSI
    for window in rsi_windows:
        delta = grouped["close"].diff()
        gain = delta.where(delta > 0, 0)
        loss = -delta.where(delta < 0, 0)
        avg_gain = gain.rolling(window=window, min_periods=1).mean()
        avg_loss = loss.rolling(window=window, min_periods=1).mean()
        rs = avg_gain / avg_loss
        df[f"rsi_{window}"] = 100 - (100 / (1 + rs))

    # Apply Bollinger Bands
    for window in bollinger_windows:
        rolling_mean = grouped["close"].transform(lambda x: x.rolling(window=window, min_periods=1).mean())
        rolling_std = grouped["close"].transform(lambda x: x.rolling(window=window, min_periods=1).std())
        df[f"bollinger_upper_{window}"] = rolling_mean + (2 * rolling_std)
        df[f"bollinger_lower_{window}"] = rolling_mean - (2 * rolling_std)

    # Apply MACD (Moving Average Convergence Divergence)
    # Apply MACD (Moving Average Convergence Divergence)
    for macd in macd_windows:
        short_window = macd["short"]
        long_window = macd["long"]
        signal_window = macd["signal"]

        df[f"macd_{short_window}_{long_window}"] = (
            grouped["close"].transform(lambda x: x.ewm(span=short_window, adjust=False).mean()) -
            grouped["close"].transform(lambda x: x.ewm(span=long_window, adjust=False).mean())
        )

        df[f"macd_signal_{short_window}_{long_window}"] = (
            df[f"macd_{short_window}_{long_window}"].ewm(span=signal_window, adjust=False).mean()
        )

    return df