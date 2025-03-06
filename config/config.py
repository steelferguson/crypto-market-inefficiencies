import os

# PostgreSQL Database Connection Details
DB_NAME = "crypto_data"
DB_USER = "steelferguson"  # Your PostgreSQL username
DB_PASSWORD = os.getenv("DB_PASSWORD")  # Load from environment variable
DB_HOST = "localhost"
DB_PORT = "5432"

# Symbols for KuCoin (Removing SHELL, KAITO, TRUMP)
KUCOIN_SYMBOLS = [
    "BTC/USDT", "ETH/USDT", "XRP/USDT", "SOL/USDT", "BNB/USDT",
    "LTC/USDT", "DOGE/USDT", "RUNE/USDT", "SUI/USDT", "ADA/USDT",
    "USDC/USDT"
]

# Symbols for Kraken (Removing MATIC)
KRAKEN_SYMBOLS = []

# Number of days for historical data retrieval in fetch_historical_data
DAYS_HISTORY = 60  

# Timeframe for OHLCV data ("1h" = hourly, smaller intervals available)
TIMEFRAME = "1m"  # Can be "5m", "15m", "1h", "4h", "1d", etc.

# Target features (in long table)
FUTURE_WINDOWS = [5, 15]
TARGET_THRESHOLDS = [0.01, 0.05]

# Feature Engineering Configuration (in long table)
MA_WINDOWS = [5, 15, 30, 60*2, 60*24]
EMA_WINDOWS = [10, 15, 50, 60*24]
MOMENTUM_PERIODS = [5, 15, 60]
VOLATILITY_WINDOWS = [15, 60, 60*24]
VOLUME_WINDOWS = [15, 60, 60*24]
RSI_WINDOWS = [15, 60, 60*24]
BOLLINGER_WINDOWS = [15, 60, 60*24]
MACD_WINDOWS = [
    {"short": 36, "long": 72, "signal": 36},  # Standard MACD
    {"short": 5, "long": 20, "signal": 5},   # Shorter-term MACD
]

# Wide table final features
FEATURE_COLUMNS = [
    "timestamp", "symbol", "sma_15", "sma_1440",
    "ema_15", "ema_50", 
    "price_momentum_5", "price_momentum_15", "price_momentum_60",
    "roc_15", "roc_60",
    "volatility_60",
    "volume", "volume_rolling_mean_15", "volume_rolling_mean_60", 
    "volume_change_5",
    "rsi_15", "rsi_1440",
    "bollinger_upper_60", "bollinger_lower_60",
    "macd_5_20", 
    "increase_1pct_15min"  # Target variable
]

# Wide table cross coin features
CROSS_COIN_FEATURES = [
    "momentum_15", "momentum_60",
    "roc_15", "roc_60",
    "sma_1440",
    "rsi_1440",
    "volume_rolling_mean_60"
]

FINAL_SELECTED_COINS = [
    "BTC/USDT", "ETH/USDT", "SOL/USDT", 
    "BNB/USDT", "XRP/USDT", "ADA/USDT", "DOGE/USDT"
]

TARGET_COLUMNS = [
    "ada_increase_1pct_15min",
    "bnb_increase_1pct_15min",
    "btc_increase_1pct_15min",
    "doge_increase_1pct_15min",
    "eth_increase_1pct_15min",
    "sol_increase_1pct_15min", 
    "xrp_increase_1pct_15min"
]