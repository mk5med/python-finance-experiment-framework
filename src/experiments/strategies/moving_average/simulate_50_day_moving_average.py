import json
from typing import Callable, List

import sqlalchemy
from core.helpers.prettyFromToProfitPrint import printFromToProfit

from core.simulation.MarketSimulation import MarketSimulation
from experiments.Experiment import Experiment
from experiments.strategies.moving_average.MovingAverageSimulation import (
    MovingAverageSimulation,
)

from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor
from functools import partial
import pandas as pd

from experiments.strategies.moving_average.analyseResults import analyseResults

INITIAL_CAPITAL = 1000
MOVING_AVERAGE_WINDOW = 50


def __runOnTicker(
    createConnection: Callable[[], sqlalchemy.engine.Engine], ticker: str
) -> MovingAverageSimulation:
    engine = createConnection()
    with engine.connect() as db:
        simulationBase = MovingAverageSimulation(
            movingAverageWindow=MOVING_AVERAGE_WINDOW, initialCapital=INITIAL_CAPITAL
        )
        simulation = MarketSimulation(db, "2019-01-01", [ticker])
        simulation.setAction(simulationBase.simulate)
        simulation.start()  # Run the simulation

        # Print the results
        printFromToProfit(ticker, simulationBase.initialCapital, simulationBase.cash)

        return simulationBase


def __getTickers(size: int = 50):
    """
    Resolves tickers and restricts the subset
    """
    tickers = None
    with open("../tickers.txt") as f:
        tickers = json.load(f)

    tickers = tickers[:size]
    return tickers


def __runSimulationOnTickers(
    createConnection: Callable[[], sqlalchemy.engine.Engine], tickers: List[str]
):
    result = []
    for ticker in tickers:
        result.append(partial(__runOnTicker, createConnection)(ticker))
    return result


def __start(createConnection: Callable[[], sqlalchemy.engine.Engine]) -> None:
    tickers = __getTickers()
    results = __runSimulationOnTickers(createConnection, tickers)

    _r = []
    for index, result in enumerate(results):
        _r.extend(analyseResults(tickers[index], result))

    return pd.concat(_r, axis=1).T


def __createConnection() -> sqlalchemy.engine.Engine:
    engine = sqlalchemy.create_engine(
        f"sqlite+pysqlite:///simulationDB.sqlite3",
        connect_args={"check_same_thread": False},
    )
    return engine


experiment = Experiment(
    experimentID="50-day-moving-average",
    experimentName="50 Day Moving Average",
    experimentDescription="",
)

experiment.setData(__createConnection)
experiment.setSimulation(__start)
