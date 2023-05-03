from typing import Callable
import sqlalchemy
from core.lib.ShareGroupTransactionChain import ShareGroupTransactionChain
from core.lib.tools.movingAverage import MovingAverage
from core.simulation import SimulationState
from core.simulation import MarketSimulation
from experiments.Experiment import Experiment

movingAverage = MovingAverage(10)
portfolio = ShareGroupTransactionChain()
cash: float = 1000
lastAction = 0


def simulate(stopCallback, simulationState: SimulationState, tickers):
    global cash
    global lastAction
    price = simulationState.getTickerPrice(tickers[0])

    # Skip this entry
    # Cases:
    # - No more data
    # - No data for the current simulation date
    if price == None:
        return

    (index, date, openPrice, high, low, closePrice, adjClose, volume) = price
    adjustedPrice: float = (openPrice + closePrice) / 2
    historicalAveragePrice = movingAverage.average()

    movingAverage.addData(adjustedPrice)
    if historicalAveragePrice == -1:
        # No average available
        return

    if adjustedPrice > historicalAveragePrice:
        ...
        if lastAction == -1:
            return

        ableToBuy: float = cash / adjustedPrice
        if ableToBuy == 0:
            return
        # Buy
        cost = portfolio.buy((adjustedPrice, ableToBuy))
        print(
            f"{simulationState.currentDate}: Buying {ableToBuy} for ${adjustedPrice * ableToBuy} @ {adjustedPrice}"
        )
        cash -= cost
        lastAction = -1
    else:

        # Able to sell
        if portfolio.ownedStocks() == 0:
            return
        portfolio.sunkCosts()
        (profit, shareGroups) = portfolio.maximumProfitAtPrice(adjustedPrice)

        # Reason to sell
        if profit == 0:
            return

        transaction = (
            adjustedPrice,
            sum([i[1] for i in shareGroups]),
        )

        cost = portfolio.sell_multiple(transaction, shareGroups)
        cash += cost

        print(
            f"{simulationState.currentDate}: Sold at ${adjustedPrice}. Current cash",
            "${:,.2f}".format(cash),
        )
        lastAction = 1


def __createConnection() -> sqlalchemy.engine.Engine:
    engine = sqlalchemy.create_engine(
        f"sqlite+pysqlite:///simulationDB.sqlite3",
        connect_args={"check_same_thread": False},
    )
    return engine


def __start(connection: Callable[[], sqlalchemy.engine.Engine]):
    engine = connection()
    with engine.connect() as db:
        simulation = MarketSimulation(db, "2001-01-01", tickers=["BTC-CAD"])
        simulation.setAction(simulate)
        simulation.start()
        print("Status", "${:,.2f}".format(cash))


experiment = Experiment(
    experimentID="crypto-50-day-moving-average",
    experimentName="50-day moving average in crypto",
    experimentDescription="An experiment to monitor the performance of the 50 day moving average strategy on crypto assets",
)

experiment.setData(__createConnection)
experiment.setSimulation(__start)
