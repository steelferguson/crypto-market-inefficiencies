import pandas as pd
from sqlalchemy import create_engine
from config.config import (
    DB_NAME, DB_USER, DB_PASSWORD, DB_HOST, DB_PORT, 
    FEATURE_COLUMNS, CROSS_COIN_FEATURES, FINAL_SELECTED_COINS
) 

# Establish database connection
engine = create_engine(f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}")

# Fetch only the selected features
query = f"""
    SELECT {", ".join(FEATURE_COLUMNS)}
    FROM crypto_features
    WHERE symbol IN ({", ".join([f"'{coin}'" for coin in FINAL_SELECTED_COINS])})
    AND timestamp BETWEEN '2025-01-15' AND '2025-02-28'
"""
df = pd.read_sql(query, engine)

# Pivot to wide format
df_wide = df.pivot(index="timestamp", columns="symbol")

# Flatten MultiIndex column names
df_wide.columns = [f"{col[1].lower().split("/")[0]}_{col[0]}" for col in df_wide.columns]
df_wide.reset_index(inplace=True)

# 🟢 Add Cross-Coin Features (BTC & ETH as reference)
for coin in FINAL_SELECTED_COINS:
    if coin not in ["BTC/USDT", "ETH/USDT"]:  # We compare all others to BTC and ETH
        coin_col_prefix = coin.split("/")[0].lower()  # This keeps only "btc"
        btc_col_prefix = "btc"
        eth_col_prefix = "eth"

        # Compute cross-coin features as relative ratios
        for feature in CROSS_COIN_FEATURES:
            if f"{btc_col_prefix}_{feature}" in df_wide.columns and f"{coin_col_prefix}_{feature}" in df_wide.columns:
                df_wide[f"{coin_col_prefix}_vs_btc_{feature}"] = df_wide[f"{coin_col_prefix}_{feature}"] / df_wide[f"{btc_col_prefix}_{feature}"]

            if f"{eth_col_prefix}_{feature}" in df_wide.columns and f"{coin_col_prefix}_{feature}" in df_wide.columns:
                df_wide[f"{coin_col_prefix}_vs_eth_{feature}"] = df_wide[f"{coin_col_prefix}_{feature}"] / df_wide[f"{eth_col_prefix}_{feature}"]

# Rename columns to match config.py naming
df_wide.rename(columns={
    "price_momentum_15": "momentum_15",
    "price_momentum_60": "momentum_60"
}, inplace=True)

# Insert into PostgreSQL
df_wide.to_sql("crypto_features_wide", engine, if_exists="append", index=False, method="multi")

print("✅ Wide format features successfully inserted into crypto_features_wide table!")