#!/usr/bin/env python3

import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# S&P 500 for the past 10 years, from Yahoo Finance
data = yf.download('^GSPC', start='2013-01-01', end='2023-01-01')
data = data['Close']

# Buy and Hold Strategy
buy_and_hold_returns = data.pct_change().cumsum() #cumsum, haha

# todo: moving average crossover, random buy/hold

# Plotting the results
plt.figure(figsize=(10,5))
plt.plot(buy_and_hold_returns, label='Buy and Hold')
plt.legend()
plt.show()
