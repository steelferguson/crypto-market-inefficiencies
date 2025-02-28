import ccxt
import pandas as pd
import sqlite3 

#initialize connection with Kraken
exchange = ccxt.kraken()
symbol = "BTC/USDT"

# Open High Low Close Volume (OHLCV)
ohlcv = exchange.fetch_ohlcv(symbol, "1h", limit=100)

df = pd.DataFrame(ohlcv, columns=["timestamp", "open", "high", "low", "close", "volume"])
df["timestamp"] = pd.to_datetime(df["timestamp"], unit="ms")

print(df.head())
df.to_csv("crypto_data.csv", index=False)

# save to sq lite db 
conn = sqlite3.connect("crypto_data.db")
df.to_sql("crypto_prices", conn, if_exists="replace", index=False)
conn.close()