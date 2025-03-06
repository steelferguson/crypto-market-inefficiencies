# crypto-market-inefficiencies
A machine learning project to detect inefficiencies in the crypto market

Data: per minute prices of 7 crytpo coins with associated momentum and correlation with BTC and ETH
Target: whether the currency will increase by > X within Y minutes. Starting with 1% in 15 minutes

## Small NN: 
<img width="400" alt="image" src="https://github.com/user-attachments/assets/fe5dccdd-2d59-47e9-87bc-3238e774c65d" />

## Wider NN:
<img width="400" alt="image" src="https://github.com/user-attachments/assets/bbc65dd9-1c1b-4264-b28a-f3bcc537b7ed" />


## 7 XGBoost Models:
ada_increase_1pct_15min F1-score: 0.5706
bnb_increase_1pct_15min F1-score: 0.7044
btc_increase_1pct_15min F1-score: 0.6460
doge_increase_1pct_15min F1-score: 0.5931
eth_increase_1pct_15min F1-score: 0.6281
sol_increase_1pct_15min F1-score: 0.5648
xrp_increase_1pct_15min F1-score: 0.5575

Overall Macro F1-score: 0.6092



