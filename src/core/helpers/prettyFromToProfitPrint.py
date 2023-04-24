def printFromToProfit(ticker: str, initialCapital, endCapital):
    print(
        f"Ticker {ticker}: ${initialCapital} -> ${endCapital}"
        + f" => ${endCapital - initialCapital}"
    )
