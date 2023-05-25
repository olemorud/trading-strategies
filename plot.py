#!/usr/bin/env python3

import util
import strategies

import matplotlib.pyplot as plt
import os
import pickle
import yfinance as yf

# S&P 500 for the past 20 years, from Yahoo Finance
stock_index = "^GSPC"
start = "2003-01-01"
end = "2023-01-01"

filepath = "market_data/" + util.normalize_filename(stock_index) + ".pkl"
os.makedirs(os.path.dirname(filepath), exist_ok=True)

if os.path.isfile(filepath):
    with open(filepath, "rb") as f:
        data = pickle.load(f)
else:
    with open(filepath, "wb") as f:
        data = yf.download(stock_index, start=start, end=end)
        pickle.dump(data, f)

close_values = data['Close']

# Plotting the results
plt.figure(figsize=(10, 5))

plt.plot(
    strategies.buy_hold(close_values),
    label='Buy and Hold'
)

plt.plot(
    strategies.monkey_rolling_dice(
        close_values,
        buy_likelyhood=3,
        sell_likelyhood=1,
        snooze_likelyhood=10
    ),
    label='Random Buy/Sell/Sleep 3:1:10'
)

plt.plot(
    strategies.moving_average_crossover(
        close_values,
        slow_avg_days=200,
        fast_avg_days=50
    ),
    label='Moving Average Crossover, (200 day avg vs 50 day avg)'
)

plt.plot(
    strategies.moving_average_crossover(
        close_values,
        slow_avg_days=40,
        fast_avg_days=10
    ),
    label='Moving Average Crossover, (50 day avg vs 20 day avg)'
)

plt.legend()
plt.show()
