from lib.financeLib import (
    netAssetReturn,
    netWorth,
    ownedStocks,
    stockReturn,
    sunkCost,
    transaction_buy,
    transaction_sell,
)


class SimpleTransactionChain:
    def __init__(self):
        self.transactions = []

    def buy(self, transaction: tuple):
        return transaction_buy(transaction, self.transactions)

    def sell(self, transaction: tuple):
        return transaction_sell(transaction, self.transactions)

    def sunkCosts(self):
        return sunkCost(self.transactions)

    def ownedStocks(self):
        return ownedStocks(self.transactions)

    def netWorth(self, curPrice: float):
        return netWorth(curPrice, self.transactions)

    # def netInvestmentWorth(self, curPrice):
    #   return netWorth(curPrice, self.transactions) - sunkCost(self.transactions)

    def netAssetReturn(self, curPrice: float):
        return netAssetReturn(curPrice, self.transactions)
