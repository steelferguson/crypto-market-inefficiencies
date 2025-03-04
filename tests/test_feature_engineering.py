import pandas as pd
import pytest 
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.feature_engineering import calculate_future_returns

def test_calculate_future_returns():
    # Check calculation for same symbol
    # Mock Data: Simple Dataframe
    df = pd.DataFrame({
        "timestamp": pd.date_range(start="2025-03-01 00:00:00", periods=6, freq="1min"),
        "close": [100, 100, 102, 104, 106, 108],
        "symbol": ["test_coin"] * 6
    })

    # Run function
    result = calculate_future_returns(df, 5)

    # Assertions; Check if future return calculation is correct
    assert "future_return_5min" in result.columns
    assert round(result["future_return_5min"].iloc[0], 2) == 0.08

    # Create a DataFrame with two different symbols and repeating timestamps
    timestamps = pd.date_range(start="2025-03-01 00:00:00", periods=6, freq="1min")  # Create timestamps once
    df2 = pd.DataFrame({
        "timestamp": timestamps.tolist() * 2,  # Repeat timestamps twice
        "close": [100, 100, 102, 104, 106, 108] + [100] + [101] * 5,
        "symbol": ["test_coin"] * 6 + ["other_coin"] * 6
    })

    # Run function
    result = calculate_future_returns(df2, 5)

    # Assertions; Check if future return calculation is correct
    assert "future_return_5min" in result.columns

    # Verify calculation for "test_coin"
    test_coin_result = result[result["symbol"] == "test_coin"]
    assert round(test_coin_result["future_return_5min"].iloc[0], 2) == 0.08

    # Verify calculation for "other_coin"
    other_coin_result = result[result["symbol"] == "other_coin"]
    assert round(other_coin_result["future_return_5min"].iloc[0], 2) == 0.01

