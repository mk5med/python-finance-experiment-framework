def transaction_buy(transaction: tuple, transactions: list):
    transactions.append(transaction)


def transaction_buy_verbose(price: float, quantity: int, transactions: list):
    transaction_buy((price, quantity), transactions)


def transaction_sell(transaction: tuple, transactions: list):
    """
    Creates a sell order for Q of asset at price P.
    This is saved in the transaction chain as (P, -Q).

    >>> transactions = [(1,1)]
    >>> transaction_sell((1, 1), transactions) # Create a sell order
    >>> assert transactions[1] == (1, -1)
    """
    (price, quantity) = transaction

    assert quantity > 0

    if ownedStocks(transactions) < quantity:
        raise Exception("Selling more shares than currently owned")

    transactions.append((price, -quantity))


def transaction_sell_verbose(price: float, quantity: int, transactions: list):
    transaction_sell((price, quantity), transactions)


def sunkCost(transactions: list):
    return sum([i[0] * i[1] for i in transactions])


def ownedStocks(transactions: list):
    # print(transactions)
    return sum([i[1] for i in transactions])


def netWorth(curPrice: float, transactions: list):
    return ownedStocks(transactions) * curPrice


def stockReturn(curPrice: float, purchasePrice: float):
    return curPrice - purchasePrice


def netInvestmentWorth(curPrice: float, transactions: list):
    return netWorth(curPrice, transactions) - sunkCost(transactions)


def netAssetReturn(curPrice: float, transactions: list):
    """
    This function should tell a user how much profit
    they can make if they sell all their assets at a given price.
    This means that sell orders should be skipped as the profit has already been realised.

    Proof:
    For each transaction,
      Case 1: Buy order -> qty > 0, price >= 0
        Case 1: curPrice > price
          pos * pos -> Positive price delta. Increases profit potential
        Case 2: curPrice = price
          0 * pos -> Zero price delta. No change to profit potential
        Case 3: curPrice < price
          neg * pos -> Negative price delta. Decreases profit potential

      Case 2: Sell order -> qty < 0, price >= 0
        Case 1: curPrice > price
          pos * negative -> Negative price delta. Decreases profit potential
        Case 2: curPrice = price
          0 * neg -> Zero price delta. No change to profit potential
        Case 3: curPrice < price
          neg * neg -> Positive price delta. Increases profit potential

    When a sell order exists in the transaction chain, and it is not ignored, it influences the final
    potential profit calculation. Therefore sell orders should be skipped
    """
    priceDeltas = [
        stockReturn(curPrice, price) * qty if qty > 0 else 0
        for (price, qty) in transactions
    ]
    return sum(priceDeltas)


def positiveAssetReturn(curPrice: float, transactions: list):
    """
    Determines which assets to sell such that a positive profit can be made.
    This algorithm does not consider if an asset has already been sold which
    leads to incorrect results.

    Returns: (positiveProfit, transactionsForTheProfit)
    """
    subtransactionsWithProfit = list(
        filter(lambda trans: curPrice - trans[0] >= 0, transactions)
    )
    return (
        sum([curPrice - trans[0] for trans in subtransactionsWithProfit]),
        subtransactionsWithProfit,
    )


def positiveAssetReturnAlt(curPrice: float, transactions: list):
    cost = sunkCost(transactions)
    owned = ownedStocks(transactions)
