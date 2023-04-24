import yfinance as yf
import statistics
import typing


def averageDividendPrice(data: list, entries=None):
    if entries is not None:
        data = data[-entries:]
    return statistics.mean([i.price for i in data])


def longAverageDividendPrice(data):
    return averageDividendPrice(data)


def shortAverageDividendPrice(data, lastEntries=10):
    if lastEntries is None:
        raise Exception(
            "lastEntries cannot be None. Use longAverageDividendPrice instead"
        )
    return averageDividendPrice(data, lastEntries)
