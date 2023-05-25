
import random
from typing import Sequence

import pandas as pd

BADVAL = -999999999

# Avoid floating point arithmetic errors
def microcents(usd: float) -> int:
    return int(usd * 100 * 1000)


# Buy and Hold Strategy
def buy_hold(prices: pd.Series) -> pd.Series:
    return prices.map(lambda x: x / prices[0])


# dice roll will buy/hold and sell randomly, and always has enough cash
# to buy stocks. (i.e. cash can be negative).
# Will either hold the entire market or nothing, no inbetween
def dice_roll(
        prices: pd.Series,
        buy_odds=1,
        sell_odds=1,
        snooze_odds=0
) -> pd.Series:
    if type(prices) == "float":
        prices = prices.map(microcents)

    output = pd.Series(
        data=[BADVAL] * len(prices),
        copy=False,
        index=prices.index,
        dtype=prices.dtype
    )

    cash = prices[0]
    stock_value = 0
    holding = False
    rand_max = buy_odds + sell_odds + snooze_odds

    for i, market_price in prices.items():
        dart_throw = random.randint(1, rand_max)

        if (dart_throw <= buy_odds) and not holding:
            cash -= market_price
            holding = True

        elif (dart_throw <= buy_odds + sell_odds) and holding:
            cash += market_price
            holding = False

        stock_value = market_price if holding else 0

        output[i] = (cash + stock_value)

    return output.map(lambda x: x / prices[0])


# https://www.nasdaq.com/glossary/g/golden-cross
# https://www.nasdaq.com/glossary/d/death-cross
# Assumes you blindly follow moving average crossover
def moving_avg_crossover(prices: pd.Series, slow_avg_days=200, fast_avg_days=50) -> pd.Series:
    def last_n_elem_avg(arr: Sequence[int], n: int, index: int) -> float:
        if index < n:
            return sum(arr[ : index+1]) // (index+1)
        else:
            return sum(arr[index-n : index]) // n

    prices = prices.map(microcents)

    output = pd.Series(
        data=[BADVAL] * len(prices),
        copy=False,
        index=prices.index,
    )

    cash = prices[0]
    stock_value = 0
    holding = False

    for i, (date, market_price) in zip(range(len(prices)), prices.items()):
        fast_avg = last_n_elem_avg(prices, fast_avg_days, i)
        slow_avg = last_n_elem_avg(prices, slow_avg_days, i)

        gold_cross = fast_avg >= slow_avg
        death_cross = not gold_cross

        if gold_cross and not holding:
            cash -= market_price
            holding = True

        elif death_cross and holding:
            cash += market_price
            holding = False

        stock_value = market_price if holding else 0

        output[date] = (cash + stock_value)

    return output.map(lambda x: x / prices[0])



