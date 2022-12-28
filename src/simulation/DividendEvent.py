import typing
import simulation.MarketSimulationEventBase
from simulation.SimulationState import SimulationState


class DividendEvent(simulation.MarketSimulationEventBase.MarketSimulationEvent):
    def event(
        self,
        stopCallback: typing.Callable[[], None],
        simulationState: SimulationState,
        tickers: typing.List[str],
    ) -> None:
        # 1. Get Ex-Dividend date
        # 2. Check if Ex-dividend date matches the current date
        # 3. If it does, add the appropriate amount to cash: dividend * ownedTickers
        # 4. Continue
        revenue = 0
        # Loop through all assets in the portfolio
        for tickerName in simulationState._portfolio.tickers:
            data = simulationState.getDividendData(tickerName)

            # If the ex-dividend date is the current day
            if data.keys()[-1] == simulationState.currentDate:
                ticker = simulationState._portfolio.tickers[tickerName]
                owned = ticker.transactions.ownedStocks()

                # Record the revenue event
                revenue += data[-1] * owned

        simulationState.setCash(simulationState.getCash() + revenue)
