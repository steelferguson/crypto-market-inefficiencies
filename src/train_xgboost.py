import xgboost as xgb
from sklearn.model_selection import train_test_split
from sklearn.metrics import f1_score
import numpy as np
import pandas as pd
from config.config import TARGET_COLUMNS

# Load processed data
df = pd.read_csv("data/crypto_features_wide.csv")

# 🔍 Handle Missing & Infinite Values
df.fillna(0, inplace=True)
df.replace([np.inf, -np.inf], 0, inplace=True)

# Define features & target columns
FEATURE_COLUMNS = [col for col in df.columns if col not in ["timestamp"] + TARGET_COLUMNS]

# Convert to NumPy arrays
X = df[FEATURE_COLUMNS].values
y = df[TARGET_COLUMNS].values

# Train/Test Split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Store models & predictions
xgb_models = {}
y_preds = {}

# Train a separate model for each target variable
for i, target in enumerate(TARGET_COLUMNS):
    print(f"Training XGBoost for {target}...")

    # Define model
    xgb_model = xgb.XGBClassifier(
        n_estimators=200,
        max_depth=6,
        learning_rate=0.01,
        objective="binary:logistic",
        eval_metric="logloss",
        use_label_encoder=False
    )

    # Train model
    xgb_model.fit(X_train, y_train[:, i])

    # Store model
    xgb_models[target] = xgb_model

    # Make predictions
    y_preds[target] = (xgb_model.predict(X_test) > 0.5).astype(int)

# Compute F1-score for each target
f1_scores = {target: f1_score(y_test[:, i], y_preds[target], average="macro") for i, target in enumerate(TARGET_COLUMNS)}

# Print Results
for target, f1 in f1_scores.items():
    print(f"{target} F1-score: {f1:.4f}")

# Compute Macro-Averaged F1-score across all targets
macro_f1 = np.mean(list(f1_scores.values()))
print(f"\nOverall Macro F1-score: {macro_f1:.4f}")