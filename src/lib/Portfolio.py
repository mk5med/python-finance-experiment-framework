import lib.ShareGroupTransactionChain
import typing


class PortfolioTicker:
    def __init__(self, name: str) -> None:
        self.name = name
        self.transactions = lib.ShareGroupTransactionChain.ShareGroupTransactionChain()


class Portfolio:
    def __init__(self) -> None:
        raise DeprecationWarning("Not implemented")
        self.tickers: typing.Dict[str, PortfolioTicker] = {}
        ...

    def getTickerRef(self, tickerName: str):
        if tickerName not in self.tickers:
            self.tickers[tickerName] = PortfolioTicker(tickerName)
        return self.tickers[tickerName]

    def buy(ticker: str, transaction):
        ...
