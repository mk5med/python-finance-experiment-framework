import yfinance as yf
import statistics
import typing


def dividendVolatility(data, entries=None):
    if entries is not None:
        data = data[-entries:]
    differences = []
    for i in range(len(data), 1):
        differences.append(data[i].price - data[i - 1].price)
    return statistics.mean(differences)


def longAverageDividendVolatility(data):
    return dividendVolatility(data)


def shortAverageDividendVolatility(data, lastEntries=10):
    if lastEntries is None:
        raise Exception(
            "lastEntries cannot be None. Use longAverageDividendVolatility instead"
        )
    return dividendVolatility(data, lastEntries)
