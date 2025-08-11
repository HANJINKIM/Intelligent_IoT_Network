import numpy as np
import torch

def series_to_supervised(values, lookback=60):
    X, y = [], []
    for i in range(len(values) - lookback):
        X.append(values[i:i+lookback])
        y.append(values[i+lookback])
    X = np.array(X, dtype=np.float32)
    y = np.array(y, dtype=np.float32)
    return X, y

def to_torch(x):
    # x: (N, T) → (T, N, 1) for LSTM(seq_len, batch, input_size)
    seq = torch.from_numpy(x).unsqueeze(-1).transpose(0, 1)
    return seq