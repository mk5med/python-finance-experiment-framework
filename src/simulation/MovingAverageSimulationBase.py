from datetime import datetime
import typing
from lib.ShareGroups import ShareGroups
from lib.tools.movingAverage import MovingAverage
from functools import partial
from simulation import SimulationState
import enum

class LastActionEnum(enum.Enum):
    nothing=0
    buy=-1
    sell=1

class MovingAverageSimulationBase:
    """
    The base logic for simulators using moving average calculations
    """

    def __init__(self, movingAverageWindow: int, initialCapital: float = 1000) -> None:
        self.movingAverage = MovingAverage(movingAverageWindow)

        self.cash = self.initialCapital = initialCapital
        self.lastAction = LastActionEnum.nothing
        self.portfolio = ShareGroups()
        self.timeStart = datetime.now()

    def simulate(
        self,
        stopCallback: typing.Callable[[], None],
        simulationState: SimulationState,
        tickers: typing.List[str],
    ) -> None:

        price = simulationState.getTickerPrice(tickers[0])

        # Skip this entry
        # Cases:
        # - No more data
        # - No data for the current simulation date
        if price == None:
            return

        (index, date, openPrice, high, low, closePrice, adjClose, volume) = price
        if (datetime.now() - self.timeStart).seconds // 60 >= 1:
            self.timeStart = datetime.now()
            print(tickers, date)

        # Normalize the price for the day
        adjustedPrice: float = (openPrice + closePrice) / 2
        historicalAveragePrice = self.movingAverage.average()

        self.movingAverage.addData(adjustedPrice)
        if historicalAveragePrice == -1:
            # No average available
            return

        # If the price is greater than the historical average
        if adjustedPrice > historicalAveragePrice:
            # Exit if the last action was a buy action
            if self.lastAction == LastActionEnum.buy:
                return

            # Make the transaction and remove the cash
            self.cash -= self.__buyAction(simulationState, adjustedPrice)

            # Mark that a buy action was made
            self.lastAction = LastActionEnum.buy
        else:
            # Make the transaction and add the cash
            self.cash += self.__sellAction(simulationState, adjustedPrice)

            # Mark that a sell action was made
            self.lastAction = LastActionEnum.sell

    def __buyAction(self, simulationState: SimulationState, price: float) -> float:
        if self.cash < price:
            return 0

        # Buy
        cost = self.portfolio.buy((price, 1))

        return cost

    def __sellAction(self, simulationState: SimulationState, price: float) -> None:
        # Able to sell
        if self.portfolio.ownedStocks() == 0:
            return 0

        (profit, shareGroups) = self.portfolio.maximumProfitAtPrice(price)

        # Reason to sell
        if profit == 0:
            return 0

        for shareGroup in shareGroups:
            self.portfolio.sell_single(shareGroup)

        return profit
