import argparse
import numpy as np
import torch
import torch.nn as nn
from torch.utils.data import TensorDataset, DataLoader
from lstm_model import LSTMRegressor
from data_loader import load_series
from utils import series_to_supervised, to_torch

parser = argparse.ArgumentParser()
parser.add_argument('--lookback', type=int, default=60)
parser.add_argument('--epochs', type=int, default=5)
parser.add_argument('--batch', type=int, default=64)
parser.add_argument('--lr', type=float, default=1e-3)
args = parser.parse_args()

# 1) Load data from InfluxDB
print('Loading data from InfluxDB ...')
df = load_series('-12h')
values = df['value'].values.astype('float32')

# 2) Train/Val split
split = int(len(values)*0.8)
train_vals, val_vals = values[:split], values[split:]

# 3) To supervised
Xtr, ytr = series_to_supervised(train_vals, args.lookback)
Xva, yva = series_to_supervised(val_vals, args.lookback)

# 4) Torch datasets
train_seq = to_torch(Xtr)
val_seq = to_torch(Xva)
train_y = torch.from_numpy(ytr)
val_y = torch.from_numpy(yva)

model = LSTMRegressor()
optim = torch.optim.Adam(model.parameters(), lr=args.lr)
crit = nn.MSELoss()

for epoch in range(1, args.epochs+1):
    model.train()
    optim.zero_grad()
    pred = model(train_seq)
    loss = crit(pred, train_y)
    loss.backward()
    optim.step()

    model.eval()
    with torch.no_grad():
        val_pred = model(val_seq)
        val_loss = crit(val_pred, val_y).item()

    print(f"Epoch {epoch}/{args.epochs} - train MSE: {loss.item():.6f} | val MSE: {val_loss:.6f}")

torch.save(model.state_dict(), 'lstm.pt')
print('Saved model → lstm.pt')