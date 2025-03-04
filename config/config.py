import os

# PostgreSQL Database Connection Details
DB_NAME = "crypto_data"
DB_USER = "steelferguson"  # Your PostgreSQL username
DB_PASSWORD = os.getenv("DB_PASSWORD")  # Load from environment variable
DB_HOST = "localhost"
DB_PORT = "5432"

# Symbols for KuCoin
KUCOIN_SYMBOLS = [
    "BTC/USDT", "ETH/USDT", "XRP/USDT", "SOL/USDT", "BNB/USDT",
    "LTC/USDT", "DOGE/USDT", "RUNE/USDT", "SUI/USDT", "ADA/USDT",
    "USDC/USDT", "TRUMP/USDT", "KAITO/USDT", "SHELL/USDT"
]

# Symbols for Kraken
KRAKEN_SYMBOLS = ["MATIC/USDT"]  # List of one symbol for now

# Number of days for historical data retrieval in fetch_historical_data
DAYS_HISTORY = 60  

# Timeframe for OHLCV data ("1h" = hourly, smaller intervals available)
TIMEFRAME = "1m"  # Can be "5m", "15m", "1h", "4h", "1d", etc.

# Feature Engineering Configuration
MA_WINDOWS = [5, 15, 30, 60*2, 60*24]
EMA_WINDOWS = [10, 15, 50, 60*24]
MOMENTUM_PERIODS = [5, 30]
VOLATILITY_WINDOWS = [15, 60, 60*24]
VOLUME_WINDOWS = [15, 60, 60*24]