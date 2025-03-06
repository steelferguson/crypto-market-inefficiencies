import pandas as pd
import matplotlib.pyplot as plt

# Load the dataset
df = pd.read_csv("data/crypto_features_wide.csv")

# Define target columns
TARGET_COLUMNS = [
    "ada_increase_1pct_15min", "bnb_increase_1pct_15min", "btc_increase_1pct_15min",
    "doge_increase_1pct_15min", "eth_increase_1pct_15min", "sol_increase_1pct_15min", "xrp_increase_1pct_15min"
]

# Compute the proportion of `1s` (true labels)
label_distribution = df[TARGET_COLUMNS].mean()

# Plot the distribution
plt.figure(figsize=(10, 6))
label_distribution.plot(kind="bar", color="skyblue", edgecolor="black")
plt.title("Proportion of '1' Labels (True) for Each Target")
plt.xlabel("Target Labels")
plt.ylabel("Proportion of '1's")
plt.ylim(0, 1)
plt.xticks(rotation=45)
plt.grid(axis="y", linestyle="--", alpha=0.7)
plt.show()

# Print exact proportions
print("\n🔢 **Exact Label Distribution:**")
print(label_distribution.to_frame(name="Proportion of 1s"))