#!/usr/bin/env python3

import util

from typing import *
import matplotlib.pyplot as plt
import numpy as np
import os
import pandas as pd
import pickle
import random
import yfinance as yf


BADVAL = -(2**31)


# Avoid floating point arithmetic errors
def microcents(usd: float) -> int:
    return int(usd * 1000_000)


# Buy and Hold Strategy
def buy_hold(prices: pd.Series) -> pd.Series:
    return prices.map(lambda x: x / prices[0])


# monkey rolling dice will buy/hold and sell randomly, and always has enough cash
# to buy stocks. (i.e. cash can be negative).
# Will either hold the entire market or nothing, no inbetween
def monkey_rolling_dice(
        prices: pd.Series,
        buy_likelyhood=1,
        sell_likelyhood=1,
        snooze_likelyhood=0
) -> pd.Series:
    prices = prices.map(microcents)
    cash = prices[0]
    stock_value = 0
    holding = False
    rand_max = buy_likelyhood + sell_likelyhood + snooze_likelyhood

    output = pd.Series(
        data=[BADVAL] * len(prices),
        copy=False,
        index=prices.index,
        dtype=prices.dtype
    )

    for i, market_price in prices.items():
        dart_throw = random.randint(1, rand_max)

        buy = dart_throw <= buy_likelyhood
        sell = dart_throw <= (buy_likelyhood + sell_likelyhood)

        if buy and not holding:
            cash -= market_price
            holding = True

        elif sell and holding:
            cash += market_price
            holding = False

        stock_value = market_price if holding else 0

        output[i] = (cash + stock_value)

    return output.map(lambda x: x / prices[0])


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

# buy and hold
plt.plot(
    buy_hold(close_values),
    label='Buy and Hold'
)

# monkey rolling dice
plt.plot(
    monkey_rolling_dice(
        close_values,
        buy_likelyhood=3,
        sell_likelyhood=1,
        snooze_likelyhood=100
    ),
    label='Random Buy/Sell/Sleep 3:1:10'
)

plt.legend()
plt.show()
