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
DAYS_HISTORY = 10  

# Timeframe for OHLCV data ("1h" = hourly, smaller intervals available)
TIMEFRAME = "1m"  # Can be "5m", "15m", "1h", "4h", "1d", etc.