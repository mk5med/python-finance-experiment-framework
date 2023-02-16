import typing
import pandas as pd
import sqlalchemy
import yfinance as yf
from extra.ThreadPool import ThreadPool
from extra.threadTypes import TaskType
from lib.Portfolio import Portfolio
from simulation import SimulationState, MarketSimulation
import queue

from simulation.events import DividendEvent

taskQueue = typing.cast(TaskType, queue.Queue())
resultQueue: "queue.Queue[typing.Any]" = queue.Queue()
failedTaskQueue = typing.cast(TaskType, queue.Queue())
pool: ThreadPool = ThreadPool(5, taskQueue, failedTaskQueue, print)


def findBestAsset() -> None:
    ...


def getExDividendDate() -> None:
    # If it is a live feed, check ticker.info
    # If it is an old feed, check the next date on which a dividend was returned
    ...


def simulate(
    stopSimulation: typing.Callable[[], None],
    simulationState: SimulationState,
    tickers: typing.List[str],
) -> None:
    # 1) Create a portfolio with the best dividend return
    # 2) Evaluate the portfolio periodically and rebalance as needed
    #   A dividend portfolio will be rebalanced every time the price changes
    #   this can happen either per minute or per day
    #   we will use per day to speed up the simulation.
    #   To account for fluctuations we will use the average between the open and close
    # 3) For the dividend to come in it must be held until the ex-dividend date.
    #    where do we find the upcoming ex-dividend date?
    ...


def start(createConnection: typing.Callable[[], sqlalchemy.engine.Engine]) -> None:
    global pool
    import json

    engine = createConnection()
    DIVIDEND_YIELD = 0.1

    with engine.connect() as db:
        with open("../tickers.txt") as f:
            # Load all the tickers
            allTickers = json.load(f)
            portfolio = Portfolio()
            simulation = MarketSimulation(db, "2019-01-07", tickers=allTickers)
            simulation.simulationState.setPortfolio(portfolio=portfolio)
            simulation.setAction(simulate)

            # Listen for dividend events
            simulation.registerEvent(DividendEvent.DividendEvent())

            print("Initialising experiment portfolio")
            tickers = simulation.simulationState.getAvailableTickers()

            for ticker in tickers:
                dData = simulation.simulationState.getDividendData(ticker)

                # Skip if there is no dividend data
                if len(dData) == 0:
                    continue

                # # Skip TRL
                # if "TRL" in ticker:
                #     continue

                data = simulation.simulationState.getTickerPrice(ticker)
                price = data[5]
                lastDividend = dData[-1]

                dividendYield = lastDividend / price
                # If the yield is greater than or equal to the DIVIDEND_YIELD
                if dividendYield >= DIVIDEND_YIELD:
                    simulation.simulationState.buy(ticker, 1)

            print(f"Found {len([i for i in portfolio.tickers])} assets")
            print("Started market simulation")

            # Get the amount paid to initialize the portfolio
            initialisationCost = abs(simulation.simulationState.getCash())

            # Reset cash to 0
            simulation.simulationState.setCash(0)

            simulation.start()
            endCash = simulation.simulationState.getCash()

            return {
                "profit": endCash,
                "sunkCost": initialisationCost,
                "roi": endCash / initialisationCost,
            }
