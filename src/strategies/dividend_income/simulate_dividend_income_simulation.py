import typing
import pandas as pd
import sqlalchemy
import yfinance as yf
from extra.ThreadPool import ThreadPool
from extra.threadTypes import TaskType
from lib.Portfolio import Portfolio
from simulation import DividendEvent, SimulationState, MarketSimulation
import queue

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

    for ticker in tickers[:5]:
        s = simulationState.getTickerPrice(ticker)
    ...


def start(createConnection: typing.Callable[[], sqlalchemy.engine.Engine]) -> None:
    global pool
    import json

    engine = createConnection()
    with engine.connect() as db:
        with open("../tickers.txt") as f:
            # Load all the tickers
            tickers = json.load(f)
            portfolio = Portfolio()
            simulation = MarketSimulation(db, "2022-01-07", tickers=tickers)
            simulation.simulationState.setPortfolio(portfolio=portfolio)
            simulation.setAction(simulate)
            simulation.registerEvent(DividendEvent.DividendEvent())

            simulation.simulationState.buy("INO-UN.TO", 100)
            initCash = simulation.simulationState.getCash()
            simulation.start()
            endCash = simulation.simulationState.getCash()
            return {
                "profit": endCash - initCash,
                "sunkCost": initCash,
                "roi": (endCash - initCash) / initCash,
            }
            del pool
