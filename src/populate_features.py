from sqlalchemy import create_engine
import pandas as pd
from config.config import DB_NAME, DB_USER, DB_PASSWORD, DB_HOST, DB_PORT
from src.feature_engineering import calculate_features, calculate_future_returns

# Create SQLAlchemy engine
engine = create_engine(f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}")

# Define SQL query to fetch data
query = """
    SELECT timestamp, symbol, close, volume
    FROM crypto_prices
    WHERE timestamp BETWEEN '2025-01-15' AND '2025-02-28'
"""

# Load data into a DataFrame
df = pd.read_sql(query, engine)

# Apply feature engineering
df = calculate_features(df)
df = calculate_future_returns(df)

# Insert into crypto_features table
df.to_sql("crypto_features", engine, if_exists="append", index=False, method="multi")

print("✅ Features successfully inserted into crypto_features table!")