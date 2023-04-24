from helpers.balancer2 import balance_break_even, nToMakeProfit
from lib.financeLib import (
    transaction_buy,
    netAssetReturn,
    netWorth,
    ownedStocks,
    positiveAssetReturn,
    sunkCost,
)


def stringifySimpleTransaction(transaction: tuple):
    return f"(${transaction[0]} x{transaction[1]})"


def printStatus(curPrice: float, TRANSACTIONS: list):
    print("#" * 10)
    print(f"Shares owned: {ownedStocks(TRANSACTIONS)}")
    print(f"Current price: ${curPrice}")
    print(f"Sunk costs: ${sunkCost(TRANSACTIONS)}")
    print(f"Net worth: ${netWorth(curPrice, TRANSACTIONS)}")
    print(f"Investment return: ${netAssetReturn(curPrice, TRANSACTIONS)}")

    [posAssetReturn, subTransactions] = positiveAssetReturn(curPrice, TRANSACTIONS)

    print(
        f"Positive stock return: ${posAssetReturn} if {ownedStocks(subTransactions)}/{ownedStocks(TRANSACTIONS)} are sold"
    )
    print("#" * 10)
