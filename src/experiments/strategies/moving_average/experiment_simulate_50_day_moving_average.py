import json
from typing import Callable, List
import typing

import sqlalchemy
from core.helpers.prettyFromToProfitPrint import printFromToProfit

from core.simulation.MarketSimulation import MarketSimulation
from experiments.Experiment import Experiment
from experiments.strategies.moving_average.MovingAverageSimulation import (
    MovingAverageSimulation,
)

from concurrent.futures import ProcessPoolExecutor
from functools import partial
import pandas as pd

from experiments.strategies.moving_average.analyseResults import analyseResults
import plotly
import plotly.express
import plotly.subplots

INITIAL_CAPITAL = 1000
MOVING_AVERAGE_WINDOW = 50


def __runOnTicker(
    createConnection: Callable[[], sqlalchemy.engine.Engine], ticker: str
) -> MovingAverageSimulation:
    with createConnection().connect() as db:
        simulationBase = MovingAverageSimulation(
            movingAverageWindow=MOVING_AVERAGE_WINDOW, initialCapital=INITIAL_CAPITAL
        )
        simulation = MarketSimulation(db, "2000-01-01", [ticker])
        simulation.setAction(simulationBase.simulate)
        simulation.start()  # Run the simulation

        # Print the results
        printFromToProfit(ticker, simulationBase.initialCapital, simulationBase.cash)

        return simulationBase


def __getTickers(size: typing.Union[int, None] = 50):
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
    p = partial(__runOnTicker, createConnection)
    with ProcessPoolExecutor(max_workers=6) as executor:
        result = executor.map(p, tickers)
    # for ticker in tickers:
    #     result.append(p(ticker))
    return result


def __start(createConnection: Callable[[], sqlalchemy.engine.Engine]) -> None:
    tickers = __getTickers(None)
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


def visualise(result: pd.DataFrame):
    """
    Result columns:
        "ticker",
        "triggered",
        "time_held",
        "buyPrice",
        "sellPrice",
        "profit",
        "instant_yield",
    """

    std = result["instant_yield"].std()
    result = result[result["instant_yield"] < std]
    result = result[".TO" in result["ticker"]]

    fig = plotly.express.line(
        result,
        x="triggered",
        y="instant_yield",
        color="ticker",
    )
    fig.show()


experiment = Experiment(
    experimentID="50-day-moving-average",
    experimentName="50 Day Moving Average",
    experimentDescription="",
    experimentCacheNonce="v1",
)

experiment.setData(__createConnection)
experiment.setSimulation(__start)
experiment.setVisualisation(visualise)
