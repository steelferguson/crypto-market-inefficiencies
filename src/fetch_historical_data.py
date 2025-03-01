import ccxt
import psycopg2
import pandas as pd
from datetime import datetime, timedelta
from config.config import (
    KUCOIN_SYMBOLS, KRAKEN_SYMBOLS, DAYS_HISTORY, TIMEFRAME,
    DB_NAME, DB_USER, DB_PASSWORD, DB_HOST, DB_PORT
)

# Connect to PostgreSQL
conn = psycopg2.connect(
    dbname=DB_NAME,
    user=DB_USER,
    password=DB_PASSWORD,
    host=DB_HOST,
    port=DB_PORT
)

# Convert days to milliseconds (CCXT uses timestamps in ms)
since_timestamp = int((datetime.now() - timedelta(days=DAYS_HISTORY)).timestamp() * 1000)

def insert_historical_data(exchange, symbols, exchange_name):
    """Fetches and inserts historical OHLCV data from an exchange."""
    try:
        # Connect to PostgreSQL
        conn = psycopg2.connect(
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
            host=DB_HOST,
            port=DB_PORT
        )
        cursor = conn.cursor()

        for symbol in symbols:
            try:
                # Fetch historical OHLCV data
                ohlcv = exchange.fetch_ohlcv(symbol, timeframe=TIMEFRAME, since=since_timestamp, limit=1000)

                if not ohlcv:
                    print(f"No historical data for {symbol} on {exchange_name}.")
                    continue

                # Convert to Pandas DataFrame
                df = pd.DataFrame(ohlcv, columns=["timestamp", "open", "high", "low", "close", "volume"])
                df["timestamp"] = pd.to_datetime(df["timestamp"], unit="ms")

                # Insert data into PostgreSQL
                for _, row in df.iterrows():
                    cursor.execute("""
                        INSERT INTO crypto_prices (timestamp, symbol, open, high, low, close, volume)
                        VALUES (%s, %s, %s, %s, %s, %s, %s)
                        ON CONFLICT DO NOTHING;
                    """, (row["timestamp"], symbol, row["open"], row["high"], row["low"], row["close"], row["volume"]))

                print(f"Inserted {len(df)} historical rows for {symbol} from {exchange_name}")

            except Exception as e:
                print(f"Error fetching historical data for {symbol} from {exchange_name}: {e}")

        # Commit and close connection
        conn.commit()
        cursor.close()
        conn.close()

        print(f"✅ Historical data insertion from {exchange_name} completed successfully.")

    except Exception as e:
        print(f"Database connection error: {e}")

# Initialize exchanges
kucoin_exchange = ccxt.kucoin()
kraken_exchange = ccxt.kraken()

# Fetch and insert historical data
insert_historical_data(kucoin_exchange, KUCOIN_SYMBOLS, "KuCoin")
insert_historical_data(kraken_exchange, KRAKEN_SYMBOLS, "Kraken")