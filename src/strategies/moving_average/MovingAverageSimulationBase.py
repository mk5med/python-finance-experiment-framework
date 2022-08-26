from datetime import datetime
from lib.sharegroups import ShareGroups
from lib.tools.movingAverage import MovingAverage
from functools import partial
from simulation import SimulationState


class MovingAverageSimulationBase:
    def __init__(self, movingAverageWindow: int, initialCapital=1000):
        self.movingAverage = MovingAverage(movingAverageWindow)

        self.cash = self.initialCapital = initialCapital
        self.lastAction = 0
        self.portfolio = ShareGroups()
        self.timeStart = datetime.now()

    def simulate(self, stopCallback, simulationState: SimulationState, tickers: list):

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

        adjustedPrice = (openPrice + closePrice) / 2
        historicalAveragePrice = self.movingAverage.average()

        self.movingAverage.addData(adjustedPrice)
        if historicalAveragePrice == -1:
            # No average available
            return

        if adjustedPrice > historicalAveragePrice:
            if self.lastAction == -1:
                return

            self.cash -= self.__buyAction(simulationState, adjustedPrice)
            self.lastAction = -1
        else:
            self.__sellAction(simulationState, adjustedPrice)
            self.lastAction = 1

    def __buyAction(self, simulationState, adjustedPrice):
        if self.cash < adjustedPrice:
            return 0

        # Buy
        cost = self.portfolio.buy((adjustedPrice, 1))
        # print(
        #     f"{simulationState.currentDate}: Buying {1} for ${adjustedPrice * 1} @ {adjustedPrice}"
        # )

        return cost

    def __sellAction(self, simulationState, adjustedPrice):
        # Able to sell
        if self.portfolio.ownedStocks() == 0:
            return
        self.portfolio.sunkCosts()
        (profit, shareGroups) = self.portfolio.maximumProfitAtPrice(adjustedPrice)

        # Reason to sell
        if profit == 0:
            return

        transaction = (
            adjustedPrice,
            sum([i[1] for i in shareGroups]),
        )

        cost = self.portfolio.sell(transaction, shareGroups)
        self.cash += cost

        # print(
        #     f"{simulationState.currentDate}: Sold at ${adjustedPrice}. Current cash",
        #     "${:,.2f}".format(self.cash),
        # )
