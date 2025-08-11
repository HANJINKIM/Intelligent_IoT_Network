import argparse
import numpy as np
import torch
from lstm_model import LSTMRegressor
from data_loader import load_series
from utils import to_torch

parser = argparse.ArgumentParser()
parser.add_argument('--lookback', type=int, default=60)
parser.add_argument('--horizon', type=int, default=30)
args = parser.parse_args()

print('Loading latest series ...')
df = load_series('-2h')
values = df['value'].values.astype('float32')

model = LSTMRegressor()
model.load_state_dict(torch.load('lstm.pt', map_location='cpu'))
model.eval()

context = values[-args.lookback:].copy()
forecast = []
for _ in range(args.horizon):
    x = to_torch(context[-args.lookback:].reshape(1, -1))
    with torch.no_grad():
        yhat = model(x).numpy().ravel()[0]
    forecast.append(float(yhat))
    context = np.append(context, yhat)

print('Forecast:', forecast)