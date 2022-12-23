from lib.SimpleTransactionChain import SimpleTransactionChain
import math
import typing
from lib.typedefs import (
    TransactionListTypeDef,
    TransactionTypeDef,
    ShareGroupChainTypeDef,
)


class ShareGroups:
    @staticmethod
    def fromSimpleChain(transactions: TransactionListTypeDef):
        """
        Converts a simple transaction chain to a share group transaction chain.
        >>> transactions = [(1,1), (4,1)]
        >>> sg = ShareGroups.fromSimpleChain(transactions)
        """

        shareGroups = ShareGroups()
        for transaction in transactions:
            assert transaction[1] != 0

            if transaction[1] > 0:
                shareGroups.buy(transaction)
            else:
                sellPrice = transaction[0]
                quantity = abs(transaction[1])
                """
                Translating a single share group chain to a multi-share group chain
                is ambiguous for sells as it is unknown what level of profit the user
                considered. For example: [(1,1), (4, 1)]. sunk cost = $5. sell 1 at $3.
                Did the user make a $2 profit or a $1 loss?
                  return all = 3-1 + 3-4 = 2 - 1 = 1. sunk cost = 0
                  sell 1. $2 profit. return remaining = 3 - 4 = -1. sunk cost = $4
                  sell 1. $1 loss. return remaining = 3 - 1 = 2. sunk cost = $1
                Its important to note that sometimes people sell with the intention of making a loss (e.g: cut their losses).
                  In these cases the user can alter the sharegroup transaction chain to update the appropriate information.
                We can do a pessimist approach which selects buckets that create the least profit, thus
                allowing the potential profits in this system to be higher.
                """
                groups = [price for price in shareGroups.groups]

                # Pessimist approach: Sort from largest to smallest
                # This minimises profit of sold assets and retains valuable assets in the system
                groups.sort()
                groups = groups[::-1]

                breakDown = []
                for price in groups:
                    # Exit if the entire quantity has been accounted for
                    if quantity == 0:
                        break
                    # Sell as many shares in this group as possible
                    # such that quantity approaches zero

                    # The quantity is higher than or equal to the current bucket
                    if quantity >= shareGroups.groups[price]:
                        breakDown.append((price, shareGroups.groups[price]))
                        quantity -= shareGroups.groups[price]
                    else:
                        breakDown.append((price, quantity))
                        quantity = 0

                assert (
                    quantity == 0
                ), f"No more share groups available to sell {quantity}. Ensure that the transaction chain is complete and correct."
                shareGroups.sell_multiple((sellPrice, abs(transaction[1])), breakDown)

        return shareGroups

    @staticmethod
    def fromShareGroupChain(transactions: ShareGroupChainTypeDef):
        shareGroups = ShareGroups()
        for transaction in transactions:
            if transaction[0] == "buy":
                shareGroups.buy(transaction[1])
            elif transaction[0] == "sell":
                shareGroups.sell_multiple(transaction[1], transaction[2])
            else:
                raise Exception(f"Unsupported transaction type: '{transaction[0]}'")

    def __init__(self):
        self.simpleTransactions = SimpleTransactionChain()
        self.groups: typing.Dict[float, float] = {}
        self.shareGroupTransactionChain: ShareGroupChainTypeDef = []

    def buy(self, transaction: TransactionTypeDef) -> float:
        """
        Register a buy order for the asset. Transaction is a tuple containing (Price, Quantity)
        >>> ShareGroups().buy((0.5,2))
        1.0
        """
        (price, qty) = transaction
        assert price >= 0
        assert qty > 0

        # Create the price group if it does not exist
        if price not in self.groups:
            self.groups[price] = 0

        # Increase the size of the price group
        self.groups[price] += qty

        # Record the transaction
        self.simpleTransactions.buy(transaction)
        self.shareGroupTransactionChain.append(
            (
                "buy",
                transaction,
            )
        )

        # Return the final cost
        return price * qty

    def sell_multiple(
        self, transaction: TransactionTypeDef, breakDown: TransactionListTypeDef
    ):
        """
        @deprecated

        Register a sell order for the asset. Transaction is a tuple containing (Price, Quantity)
        and the breakdown is a list of tuples containing the share group and quantity within the sharegroup
        to sell [(price_i, quantity_i)] where i is an index in the list.

        Requirements:
            Quantity == sum(quantity_i)

            Price == sum(price_i * quantity_i)
        """
        assert type(transaction) == tuple
        assert type(breakDown) == list

        (totalPrice, totalQty) = transaction
        assert totalPrice >= 0
        assert totalQty > 0

        # Validate the quantities are correct
        assert totalQty == sum(
            [assetGroup[1] for assetGroup in breakDown]
        ), f"The total quantity of assets to sell ({totalQty}) is\
            not equal to the assets in the breakdown ({sum([assetGroup[1] for assetGroup in breakDown])}). {breakDown}"

        # assert totalPrice == sum(
        #     [assetGroup[0] * assetGroup[1] for assetGroup in breakDown]
        # ), f"The total price of assets to cell ({totalPrice}) is not equal to the profits of assets in the breakdown. {breakDown}"

        for subTransaction in breakDown:
            self.sell_single(subTransaction)

        # Record the transaction
        self.simpleTransactions.sell(transaction)
        self.shareGroupTransactionChain.append(("sell", transaction, breakDown))
        return totalPrice

    def sell_single(self, transaction: TransactionTypeDef):
        (price, qty) = transaction
        assert price in self.groups  # Check that the referenced tranche exists
        assert (
            qty <= self.groups[price]
        )  # Check that the referenced tranche has enough quantity to be sold
        self.groups[price] -= qty
        return price

    def maximumProfitAtPrice(self, possiblePrice: float):
        """
        Calculate the highest possible returns for the current sharegroups for the asset
        at a given price point.
        """
        # Find all groups that have a positive return at the possible price
        positiveGroups = list(
            filter(
                lambda price: price < possiblePrice and self.groups[price] > 0,
                [price for price in self.groups],
            )
        )
        shareGroups = [(i, self.groups[i]) for i in positiveGroups]
        profits: float = 0
        for i in positiveGroups:
            profits += self.groups[i] * (possiblePrice - i)

        return (profits, shareGroups)

    def priceForReturn(self, retVal: float):
        """
        Calculate the asset price required to get the desired return value

        retVal = Sum_{i=0}^{j} {(Price - p_i) * q_i}
        retVal = (Price-p_0) * q_0 + (Price-p_1) * q_1 + ... + Pricei-p_j) * q_j
        retVal = Price * q_0 - p_0 * q_0 + Price * q_1 - p_1 * q_1 + ... + Price * q_j - p_j * q_j
        retVal = Price * (q_0 + q_1 + ... + q_j) - (p_0 * q_0 + p_1 * q_1 + ... + p_j * q_j)
        retVal = Price * ownedStocks() - sunkCosts()
        """
        if len(self.simpleTransactions.transactions) == 0:
            return None
        return (retVal + self.sunkCosts()) / self.ownedStocks()

    def sunkCosts(self) -> float:
        """
        Returns the amount of money that has been spent to purchase the current
        share group set.

        This calculation does not consider sold assets. For example, selling an
        asset at a loss will not influence the sunk cost in any way other than to
        show the decrease in size of the share group
        """
        return sum([self.groups[price] * price for price in self.groups])

    def ownedStocks(self) -> float:
        """
        Returns the amount of stocks owned in the set of sharegroups.

        The original function was `O(N)` where `N` is the size of the transaction list.
        This new function is also `O(M)` but `M` is generally less than `N` as transactions
        are grouped together
        """
        return sum([self.groups[price] for price in self.groups])

    def transactionForReturnAtPrice(
        self, curPrice: float, futurePrice: float, retVal: float
    ) -> TransactionTypeDef:
        """
        Calculate the quantity of shares at `curPrice` to purchase
        such that when `curPrice` equals `futurePrice` the sharegroups return will be equal to `retVal`
        """
        missingValue = retVal - self.netAssetReturn(futurePrice)
        priceChange = futurePrice - curPrice

        assert missingValue >= 0
        assert priceChange >= 0

        return (curPrice, (missingValue / priceChange))

    def netAssetReturn(self, curPrice: float) -> float:
        """
        Calculate the asset return/value of the current sharegroups.
        This considers the size of each owned share group.

        What if someone sold an asset at a loss. Should that be considered in net asset return?
        """
        return sum([(curPrice - price) * self.groups[price] for price in self.groups])


if __name__ == "__main__":
    transactions = [(1, 1), (4, 1), (3, -1)]
    sg = ShareGroups.fromSimpleChain(transactions)
