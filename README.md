# Trading strategies plot

Plots how different trading strategies would have performed
on historical data.

![figure](plot.svg)
[![FOSSA Status](https://app.fossa.com/api/projects/git%2Bgithub.com%2Folemorud%2Ftrading-strategies.svg?type=shield)](https://app.fossa.com/projects/git%2Bgithub.com%2Folemorud%2Ftrading-strategies?ref=badge_shield)

## Assumptions

The main purpose of these plots is to see if stupidly
simple strategies will (roughly) outperform professionally
managed funds. Therefore some assumptions and
simplifications are made:

 - Assumes no trading fees on transactions.
 - Assumes that you're buying and selling the entire index. (subject to change)

## Currently implemented strategies:

### Buy and hold

Buy at start, never sell

### Dice roll buy/sell

Buy everything, sell everything or do nothing at random.

Performs worse than the buy and hold strategy, because the dice roll approach
ends up having fewer days invested in the stock market

### Moving average crossover

Buy when a short term average (e.g. 50 days) surpasses a long term average (e.g
200 days), buy. Conversely, sell when the long term average surpasses the short
term average.

Although it mitigates the losses of some market crashes, it also takes longer
to capitalize on bull runs, resulting in a worse performance. Briefly outperformed
buy and hold in the years after the
[2007-2008 financial crisis](https://en.wikipedia.org/wiki/2007%E2%80%932008_financial_crisis)


## Run

### Linux / MacOS

#### bash/zsh/sh
```sh
# Setup venv
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Run
./plot.py

# deactivate venv
deactivate
```

### Windows

#### PowerShell
```ps1
# Setup venv
python -m venv venv
. .\venv\Scripts\activate.ps1
python -m pip install -r requirements.txt

# Run
python .\plot.ps1

# Deactivate venv
deactivate
```

#### cmd.exe
```cmd
: Setup venv
python -m venv venv
venv\Scripts\activate.bat
pip install -r requirements.txt

: Run
python plot.py

: deactivate venv
deactivate
```


## License
[![FOSSA Status](https://app.fossa.com/api/projects/git%2Bgithub.com%2Folemorud%2Ftrading-strategies.svg?type=large)](https://app.fossa.com/projects/git%2Bgithub.com%2Folemorud%2Ftrading-strategies?ref=badge_large)