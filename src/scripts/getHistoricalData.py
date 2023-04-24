from sys import argv
import yfinance as yf
import json

if __name__ == "__main__":
    tickers = None
    with open(argv[1]) as tickerINode:
        tickers = json.load(tickerINode)

    tickersLen = len(tickers)

    for index, ticker in enumerate(tickers):
        print(f"Downloading {ticker} ({index}/{tickersLen})")
        tickerDownloadDataframe = yf.download(ticker)
        tickerDownloadDataframe.to_csv(f"../../historical_data/{ticker}.csv")
