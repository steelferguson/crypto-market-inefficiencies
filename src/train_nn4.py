import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader, TensorDataset
from sklearn.metrics import f1_score
from sklearn.preprocessing import StandardScaler
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

# ✅ Apply Standard Scaling
scaler = StandardScaler()
X_scaled = scaler.fit_transform(df[FEATURE_COLUMNS].values)  # Standardize features

# Convert data to tensors
X = torch.tensor(X_scaled, dtype=torch.float32)  # Now using scaled features
y = torch.tensor(df[TARGET_COLUMNS].values, dtype=torch.float32)


# Convert data to tensors
X = torch.tensor(df[FEATURE_COLUMNS].values, dtype=torch.float32)
y = torch.tensor(df[TARGET_COLUMNS].values, dtype=torch.float32)

# Create train/test split
train_size = int(0.8 * len(X))
X_train, X_test = X[:train_size], X[train_size:]
y_train, y_test = y[:train_size], y[train_size:]

# ✅ Check for NaNs or Infinite Values
print("Checking NaNs in X_train:", torch.isnan(X_train).sum().item())
print("Checking NaNs in y_train:", torch.isnan(y_train).sum().item())
print("Checking Inf in X_train:", torch.isinf(X_train).sum().item())
print("Checking Inf in y_train:", torch.isinf(y_train).sum().item())

# Create DataLoader
train_dataset = TensorDataset(X_train, y_train)
train_loader = DataLoader(train_dataset, batch_size=32, shuffle=True)

# 🔥 Define Neural Network Model with BatchNorm & LeakyReLU
class CryptoNN(nn.Module):
    def __init__(self, input_dim, output_dim):
        super(CryptoNN, self).__init__()
        self.fc1 = nn.Linear(input_dim, 128)
        self.bn1 = nn.BatchNorm1d(128)
        self.fc2 = nn.Linear(128, 64)
        self.bn2 = nn.BatchNorm1d(64)
        self.fc3 = nn.Linear(64, output_dim)
        self.leaky_relu = nn.LeakyReLU(0.1)  # Slope = 0.1
        self.sigmoid = nn.Sigmoid()  # Sigmoid for final output

    def forward(self, x):
        x = self.leaky_relu(self.bn1(self.fc1(x)))
        x = self.leaky_relu(self.bn2(self.fc2(x)))
        x = self.fc3(x)  # Raw logits for BCEWithLogitsLoss
        return x

# Initialize Model, Loss, Optimizer
model = CryptoNN(input_dim=len(FEATURE_COLUMNS), output_dim=len(TARGET_COLUMNS))
criterion = nn.BCEWithLogitsLoss(pos_weight=torch.tensor([5.0]))  # Adjust class imbalance
optimizer = optim.Adam(model.parameters(), lr=0.0002)

# Training Loop with F1-score Calculation
num_epochs = 400
f1_scores = []  # Store F1-scores per epoch

for epoch in range(num_epochs):
    model.train()
    epoch_labels = []
    epoch_preds = []

    for batch_X, batch_y in train_loader:
        optimizer.zero_grad()
        outputs = model(batch_X)
        loss = criterion(outputs, batch_y)
        loss.backward()
        optimizer.step()

        # Store batch predictions & labels
        epoch_labels.append(batch_y.detach().numpy())
        epoch_preds.append((torch.sigmoid(outputs).detach().numpy() > 0.75).astype(int))

    # Compute F1-score for epoch
    y_true = np.vstack(epoch_labels)
    y_pred = np.vstack(epoch_preds)
    f1 = f1_score(y_true, y_pred, average="macro")  # Macro-average F1-score
    f1_scores.append(f1)

    print(f"Epoch [{epoch+1}/{num_epochs}], Loss: {loss.item():.4f}, F1-score: {f1:.4f}")

# Final Evaluation on Test Set
model.eval()
test_preds = torch.sigmoid(model(X_test)).detach().numpy()
test_preds = (test_preds > 0.5).astype(int)  # Convert to binary labels
test_f1 = f1_score(y_test.numpy(), test_preds, average="weighted")
print(f"\nFinal Test F1-score: {test_f1:.4f}")

# ✅ Plot F1-score over epochs
import matplotlib.pyplot as plt
plt.figure(figsize=(8, 5))
plt.plot(range(1, num_epochs + 1), f1_scores, marker='o', linestyle='-', color='b')
plt.xlabel("Epoch")
plt.ylabel("F1-score")
plt.title("F1-score Trend Over Training Epochs")
plt.grid()
plt.show()