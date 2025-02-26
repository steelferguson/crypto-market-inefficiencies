import ccxt
import pandas as pd

#initialize connection with Kraken
exchange = ccxt.kraken()
symbol = "BTC/USDT"

# Open High Low Close Volume (OHLCV)
ohlcv = exchange.fetch_ohlcv(symbol, "1h", limit=100)

df = pd.DataFrame(ohlcv, columns=["timestamp", "open", "high", "low", "close", "volume"])
df["timestamp"] = pd.to_datetime(df["timestamp"], unit="ms")

print(df.head())