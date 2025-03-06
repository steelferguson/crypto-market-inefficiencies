import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

# 📌 Load the dataset
df = pd.read_csv("data/crypto_features_wide.csv")

# 🔍 Check for missing values
missing_values = df.isnull().sum()
print("Missing Values:\n", missing_values[missing_values > 0])

# 🔄 Fill or Drop Missing Values (Using Forward Fill)
df.fillna(method="ffill", inplace=True)

# 📌 Define features (X) and target (y)
target_col = "btc_increase_1pct_15min"  # Target variable
features = [col for col in df.columns if col != "timestamp" and col != target_col]  # Exclude timestamp & target

X = df[features]
y = df[target_col]

# 📌 Train-Test Split (80/20)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, shuffle=False, random_state=42)

# 📌 Scale the features (Normalize for neural networks)
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

print("✅ Data Preprocessing Complete!")