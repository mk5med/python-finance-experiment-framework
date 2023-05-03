from datetime import datetime
import typing
from core.lib.ShareGroupTransactionChain import ShareGroupTransactionChain
from core.lib.tools.movingAverage import MovingAverage
from core.simulation import SimulationState
import enum


class LastActionEnum(enum.Enum):
    nothing = 0
    buy = -1
    sell = 1
    holding = 2


class ProfitEvent:
    def __init__(
        self,
        *,
        dateBought: datetime,
        dateSold: datetime,
        qty: float,
        priceBought: float,
        priceSold: float
    ):
        self.dateBought = dateBought
        self.dateSold = dateSold
        self.qty = qty
        self.priceBought = priceBought
        self.priceSold = priceSold


class MovingAverageSimulation:
    """
    The base logic for simulators using moving average calculations
    """

    def __init__(
        self, *, movingAverageWindow: int, initialCapital: float = 1000
    ) -> None:
        self.movingAverage = MovingAverage(movingAverageWindow)

        self.cash = self.initialCapital = initialCapital
        self.lastAction = LastActionEnum.nothing
        self.portfolio = ShareGroupTransactionChain()
        self.timeStart = datetime.now()
        self.events: typing.List[ProfitEvent] = []

        self.dateBought = datetime.now()
        self.priceBought = 0

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
        if openPrice is None or closePrice is None:
            return
            
        # Normalize the price for the day
        adjustedPrice: float = (openPrice + closePrice) / 2
        historicalAveragePrice = self.movingAverage.average()

        self.movingAverage.addData(adjustedPrice)
        if (
            historicalAveragePrice == -1
            or len(self.movingAverage.values) < self.movingAverage.maxLength
        ):
            # No average available
            return

        if self.lastAction != LastActionEnum.holding and (
            # If the price is greater than the historical average
            adjustedPrice
            > historicalAveragePrice
        ):

            # Make the transaction and remove the cash
            _ns = self.__buyAction(simulationState, adjustedPrice)
            self.cash -= _ns[0]

            # Mark that a buy action was made
            self.lastAction = _ns[1]

        elif (
            self.lastAction == LastActionEnum.holding
            and adjustedPrice < historicalAveragePrice
        ):
            # Make the transaction and add the cash
            _ns = self.__sellAction(simulationState, adjustedPrice)
            if _ns[1] == LastActionEnum.holding:
                return

            self.cash += _ns[0]
            # Mark that a sell action was made
            self.lastAction = _ns[1]

    def __buyAction(self, simulationState: SimulationState, price: float) -> float:
        if self.cash < price:
            return (0, self.lastAction)

        self.dateBought = simulationState.currentDate
        self.priceBought = price

        # Buy
        return (
            self.portfolio.buy((price, 1), simulationState.currentDate),
            LastActionEnum.holding,
        )

    def __sellAction(self, simulationState: SimulationState, price: float) -> None:
        # Able to sell
        if self.portfolio.ownedStocks() == 0:
            return (0, self.lastAction)

        (profit, shareGroups) = self.portfolio.maximumProfitAtPrice(price)

        # Reason to sell
        if profit == 0:
            return (0, self.lastAction)

        for shareGroup in shareGroups:
            self.portfolio.sell_single(shareGroup, simulationState.currentDate, price)

        self.events.append(
            ProfitEvent(
                dateBought=self.dateBought,
                dateSold=simulationState.currentDate,
                qty=len(shareGroups),
                priceBought=self.priceBought,
                priceSold=price,
            )
        )

        # print("sell")
        return (len(shareGroups) * price, LastActionEnum.sell, profit)
