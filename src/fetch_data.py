import os
import ccxt
import psycopg2
import pandas as pd
from datetime import datetime
from config.config import (
    KUCOIN_SYMBOLS, KRAKEN_SYMBOLS, TIMEFRAME,
    DB_NAME, DB_USER, DB_PASSWORD, DB_HOST, DB_PORT
)

def get_latest_timestamp(symbol, conn):
    """Fetches the latest timestamp for a given symbol from PostgreSQL."""
    cursor = conn.cursor()
    cursor.execute("SELECT MAX(timestamp) FROM crypto_prices WHERE symbol = %s;", (symbol,))
    latest_timestamp = cursor.fetchone()[0]
    cursor.close()

    # Convert to milliseconds if data exists, otherwise return None
    return int(latest_timestamp.timestamp() * 1000) if latest_timestamp else None

def insert_crypto_data(exchange, symbols, exchange_name):
    """Fetches and inserts only new OHLCV data from an exchange."""
    try:
        # Connect to PostgreSQL
        conn = psycopg2.connect(
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
            host=DB_HOST,
            port=DB_PORT
        )

        for symbol in symbols:
            try:
                # Get latest stored timestamp for this symbol
                since_timestamp = get_latest_timestamp(symbol, conn)

                # Fetch new OHLCV data only after the last stored timestamp
                ohlcv = exchange.fetch_ohlcv(symbol, timeframe=TIMEFRAME, since=since_timestamp)

                if not ohlcv:
                    print(f"No new data available for {symbol} on {exchange_name}.")
                    continue

                # Convert to Pandas DataFrame
                df = pd.DataFrame(ohlcv, columns=["timestamp", "open", "high", "low", "close", "volume"])
                df["timestamp"] = pd.to_datetime(df["timestamp"], unit="ms")

                # Insert new data into PostgreSQL
                cursor = conn.cursor()
                for _, row in df.iterrows():
                    cursor.execute("""
                        INSERT INTO crypto_prices (timestamp, symbol, open, high, low, close, volume)
                        VALUES (%s, %s, %s, %s, %s, %s, %s)
                        ON CONFLICT DO NOTHING;
                    """, (row["timestamp"], symbol, row["open"], row["high"], row["low"], row["close"], row["volume"]))

                conn.commit()
                cursor.close()
                print(f"Inserted {len(df)} new rows for {symbol} from {exchange_name}")

            except Exception as e:
                print(f"Error fetching new data for {symbol} from {exchange_name}: {e}")

        conn.close()
        print(f"✅ Data insertion from {exchange_name} completed successfully.")

    except Exception as e:
        print(f"Database connection error: {e}")

# Initialize exchanges
kucoin_exchange = ccxt.kucoin()
kraken_exchange = ccxt.kraken()

# Fetch and insert only new data
insert_crypto_data(kucoin_exchange, KUCOIN_SYMBOLS, "KuCoin")
insert_crypto_data(kraken_exchange, KRAKEN_SYMBOLS, "Kraken")