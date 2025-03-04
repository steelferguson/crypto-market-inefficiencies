import pandas as pd
import pytest 
import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.feature_engineering import (
    calculate_future_returns, calculate_features
)
from config.config import (
    MA_WINDOWS, EMA_WINDOWS, MOMENTUM_PERIODS, VOLATILITY_WINDOWS, VOLUME_WINDOWS
)

@pytest.fixture
def sample_data():
    """Fixture to create sample crypto data for testing."""
    timestamps = pd.date_range(start="2025-03-01 00:00:00", periods=10, freq="1min")  # Create timestamps once
    data = {
        "timestamp": timestamps.tolist() * 2,  # Repeat timestamps twice
        "close": [100, 102, 104, 106, 108, 110, 112, 114, 116, 118] + [100] + [101] * 9,
        "volume": [500, 520, 510, 530, 540, 550, 560, 570, 580, 590] + [300] * 10,
        "symbol": ["test_coin"] * 10 + ["other_coin"] * 10
    }

    return pd.DataFrame(data)

def test_calculate_future_returns(sample_data):
    # Check calculation for same symbol
    print(sample_data["symbol"].value_counts())  
    result = calculate_future_returns(sample_data, future_window=4)
    print(result.tail(20))

    # Assertions; Check if future return calculation is correct
    assert "future_return_4min" in result.columns

    # Verify calculation for "test_coin"
    test_coin_result = result[result["symbol"] == "test_coin"]
    assert round(test_coin_result["future_return_4min"].iloc[0], 2) == 0.08

    # Verify calculation for "other_coin"
    other_coin_result = result[result["symbol"] == "other_coin"]
    assert round(other_coin_result["future_return_4min"].iloc[0], 2) == 0.01


def test_calculate_features(sample_data):
    """Test all feature calculations in one function."""
    result = calculate_features(sample_data[sample_data["symbol"] == "test_coin"])

    # ✅ Check SMA calculations
    for window in MA_WINDOWS:
        assert f"sma_{window}" in result.columns, f"Missing SMA column: sma_{window}"

    # ✅ Check EMA calculations
    for window in EMA_WINDOWS:
        assert f"ema_{window}" in result.columns, f"Missing EMA column: ema_{window}"

    # ✅ Check Momentum & Rate of Change
    for period in MOMENTUM_PERIODS:
        assert f"price_momentum_{period}" in result.columns, f"Missing Momentum column: price_momentum_{period}"
        assert f"roc_{period}" in result.columns, f"Missing RoC column: roc_{period}"

    # ✅ Check Volatility
    for window in VOLATILITY_WINDOWS:
        assert f"volatility_{window}" in result.columns, f"Missing Volatility column: volatility_{window}"

    # ✅ Check Volume Features
    for window in VOLUME_WINDOWS:
        assert f"volume_rolling_mean_{window}" in result.columns, f"Missing Volume Rolling Mean column: volume_rolling_mean_{window}"

    assert "volume_change_5" in result.columns, "Missing Volume Change column: volume_change_5"

    # ✅ Verify SMA values (Example: SMA-5 should be correct)
    assert round(result["sma_5"].iloc[5], 2) == 106, "Incorrect SMA-5 calculation"

    # ✅ Verify EMA values (Example: EMA-10)
    assert round(result["ema_10"].iloc[5], 2) > 100, "Incorrect EMA-10 calculation"

    # ✅ Verify Momentum (Example: Momentum-5)
    assert result["price_momentum_5"].iloc[5] == 10, "Incorrect Momentum-5 calculation"

    print("✅ All feature engineering tests passed successfully!")