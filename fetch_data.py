import os
import ccxt
import pandas as pd
import psycopg2

# Fetch password from environment variable
DB_PASSWORD = os.getenv("DB_PASSWORD")

# Database connection details
DB_NAME = "crypto_data"
DB_USER = "steelferguson"
DB_HOST = "localhost"
DB_PORT = "5432"

# Function to insert crytpo data
def insert_crypto_data(symbol, timeframe="1h", limit=10):
    try:
        conn = psycopg2.connect(
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,  # Using environment variable
            host=DB_HOST,
            port=DB_PORT
        )
        cursor = conn.cursor()

        exhange = ccxt.kraken()
        ohlcv = exhange.fetch_ohlcv(symbol, timeframe, limit=limit)

        df = pd.DataFrame(ohlcv, columns=["timestamp", "open", "high", "low", "close", "volume"])
        df["timestamp"] = pd.to_datetime(df["timestamp"], unit="ms")

        for _, row in df.iterrows():
            cursor.execute("""
                INSERT INTO crypto_prices (timestamp, symbol, open, high, low, close, volume)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
                ON CONFLICT DO NOTHING;          
            """, (row["timestamp"], symbol, row["open"], row["high"], row["low"], row["close"], row["volume"]))
        
        conn.commit()
        cursor.close()
        conn.close()

        print(f"Inserted {len(df)} rows of {symbol} data into PostgreSQL.")

    except Exception as e:
        print(f"Error: {e}")
        
# Run the function 
insert_crypto_data("BTC/USDT", timeframe="1h", limit=10)