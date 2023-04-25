import json
from typing import Callable, List

import sqlalchemy
from core.helpers.prettyFromToProfitPrint import printFromToProfit

from core.simulation.MarketSimulation import MarketSimulation
from experiments.strategies.moving_average.MovingAverageSimulation import (
    MovingAverageSimulation,
)

from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor
from functools import partial
import pandas as pd

from experiments.strategies.moving_average.analyseResults import analyseResults

INITIAL_CAPITAL = 1000
MOVING_AVERAGE_WINDOW = 50


def _runOnTicker(
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

        # Return a summary of the results
        return pd.Series(
            data=[
                ticker,
                simulationBase.initialCapital,
                simulationBase.cash,
                simulationBase.cash - simulationBase.initialCapital,
                simulationBase.lastAction,
            ],
            index=["ticker", "initialCapital", "endCapital", "delta", "lastAction"],
        )


def getTickers(size: int = 50):
    tickers = None
    with open("../tickers.txt") as f:
        tickers = json.load(f)

    tickers = tickers[:size]
    return tickers


def runSimulationOnTickers(
    createConnection: Callable[[], sqlalchemy.engine.Engine], tickers: List[str]
):
    result = []
    for ticker in tickers:
        result.append(partial(_runOnTicker, createConnection)(ticker))
    return result


def start(createConnection: Callable[[], sqlalchemy.engine.Engine]) -> None:
    tickers = getTickers(50)
    results = runSimulationOnTickers(createConnection, tickers)

    _r = []
    for index, result in enumerate(results):
        _r.extend(analyseResults(tickers[index], result))

    return pd.concat(_r, axis=1).T
