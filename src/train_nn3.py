import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader, TensorDataset
from sklearn.metrics import f1_score
import numpy as np
import pandas as pd
from config.config import TARGET_COLUMNS

# Load processed data
df = pd.read_csv("data/crypto_features_wide.csv")

# Handle missing or infinite values
df.ffill(inplace=True)
df.fillna(0, inplace=True)
df.replace([np.inf, -np.inf], 0, inplace=True)

# Define features & target columns
FEATURE_COLUMNS = [col for col in df.columns if col not in ["timestamp"] + TARGET_COLUMNS]

# Convert data to tensors
X = torch.tensor(df[FEATURE_COLUMNS].values, dtype=torch.float32)
y = torch.tensor(df[TARGET_COLUMNS].values, dtype=torch.float32)

# Create train/test split
train_size = int(0.8 * len(X))
X_train, X_test = X[:train_size], X[train_size:]
y_train, y_test = y[:train_size], y[train_size:]

# Create DataLoader
train_dataset = TensorDataset(X_train, y_train)
train_loader = DataLoader(train_dataset, batch_size=32, shuffle=True)

# ✅ Define Wider Neural Network Model
class WideCryptoNN(nn.Module):
    def __init__(self, input_dim, output_dim):
        super(WideCryptoNN, self).__init__()
        self.fc1 = nn.Linear(input_dim, 512)
        self.bn1 = nn.BatchNorm1d(512)
        self.fc2 = nn.Linear(512, 256)
        self.bn2 = nn.BatchNorm1d(256)
        self.fc3 = nn.Linear(256, 128)
        self.bn3 = nn.BatchNorm1d(128)
        self.fc4 = nn.Linear(128, output_dim)
        
        self.leaky_relu = nn.LeakyReLU(0.1)
        self.dropout = nn.Dropout(0.3)
    
    def forward(self, x):
        x = self.leaky_relu(self.bn1(self.fc1(x)))
        x = self.dropout(x)
        x = self.leaky_relu(self.bn2(self.fc2(x)))
        x = self.dropout(x)
        x = self.leaky_relu(self.bn3(self.fc3(x)))
        x = self.fc4(x)  # No sigmoid here (BCEWithLogitsLoss will handle it)
        return x

# Initialize Model, Loss, Optimizer
model = WideCryptoNN(input_dim=len(FEATURE_COLUMNS), output_dim=len(TARGET_COLUMNS))
criterion = nn.BCEWithLogitsLoss(pos_weight=torch.tensor([5.0]))  # Give more weight to positives
optimizer = optim.Adam(model.parameters(), lr=0.0001)  # Smaller LR

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
        epoch_preds.append((torch.sigmoid(outputs).detach().numpy() > 0.5).astype(int))  # Convert probs to binary labels

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
test_f1 = f1_score(y_test.numpy(), test_preds, average="macro")
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