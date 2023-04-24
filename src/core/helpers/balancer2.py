from lib.financeLib import netAssetReturn, stockReturn
import math


def nToMakeProfit(curPrice, transactions, expectedChange, profit):
    return int(
        math.ceil(
            (profit - netAssetReturn(curPrice * (1 + expectedChange), transactions))
            / (curPrice * expectedChange)
        )
    )


def balance_break_even(curPrice, transactions, expectedChange):
    # Is it making a profit right now?
    profit = netAssetReturn(curPrice * (1 + expectedChange), transactions)

    # The portfolio is making a profit right now
    # Maybe we should calculate how to minimise risk if the price drops
    if profit > 0:
        raise Exception("Positive profit")

    out = nToMakeProfit(curPrice, transactions, expectedChange, 0)
    # if out < 0: raise Exception("Breakeven point is negative")
    return out
