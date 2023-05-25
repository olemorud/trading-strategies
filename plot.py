#!/usr/bin/env python3

import os
import pickle

import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
import yfinance as yf

import strategies
import util

# S&P 500 for the past 20 years, from Yahoo Finance
# attempt to save and load from file
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

plt.figure(figsize=(10, 5))

strategies.buy_hold(close_values) \
    .plot( label='Buy and Hold' ) \
    .yaxis.set_major_formatter( mtick.PercentFormatter(1.0) )

strategies.dice_roll(close_values, buy_odds=3, sell_odds=1, snooze_odds=10) \
    .plot( label='Random Buy/Sell/Sleep 3:1:10') \
    .yaxis.set_major_formatter( mtick.PercentFormatter(1.0) )

strategies.moving_avg_crossover(close_values, slow_avg_days=200, fast_avg_days=50) \
    .plot( label='Moving Average Crossover, (200 day avg vs 50 day avg)' ) \
    .yaxis.set_major_formatter( mtick.PercentFormatter(1.0) )

strategies.moving_avg_crossover(close_values, slow_avg_days=40, fast_avg_days=10) \
    .plot( label='Moving Average Crossover, (40 day avg vs 10 day avg)' ) \
    .yaxis.set_major_formatter( mtick.PercentFormatter(1.0) )

plt.legend()

plt.savefig("plot.svg")

plt.show()
