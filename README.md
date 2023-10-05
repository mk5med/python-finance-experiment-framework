# Finance Experiment Framework

This framework allows researchers to download public stock data and replay it to perform backtesting and performance evaluation on models.

This tool isn't ready for use.

## Installation

1. Create and enter a virtual python environment. e.g: `python3 -m venv .venv && source .venv/bin/activate`
2. Install dependencies `pip3 install -r requirements.txt`
3. Write a list of stock tickers into a file called "tickers.tsx". The format is: `["...", ...]`
3. CD into `./src`
5. Run `python3 main.py --seed` to seed the database
6. Run `python3 main.py --sim` to run the experiments