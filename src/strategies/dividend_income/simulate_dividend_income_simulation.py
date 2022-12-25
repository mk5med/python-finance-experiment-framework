import typing
import pandas as pd
import sqlalchemy
import yfinance as yf
from extra.ThreadPool import ThreadPool
from extra.threadTypes import TaskType
from simulation import SimulationState, MarketSimulation
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

    print(simulationState.currentDate)
    for ticker in tickers[:5]:
        taskQueue.put((simulationState.getTickerPrice, [ticker]))

    taskQueue.join()
    ...


def start(engine: sqlalchemy.engine.Engine) -> None:
    global pool
    import json

    with engine.connect() as db:
        with open("./tickers.txt") as f:
            tickers = json.load(f)
            simulation = MarketSimulation(db, "2022-01-01", tickers=tickers)
            simulation.setAction(simulate)

            pool.start()
            simulation.start()
            del pool
