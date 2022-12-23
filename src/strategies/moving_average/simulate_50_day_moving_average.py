import json
from typing import Callable, List

import sqlalchemy

from simulation.AssetSimulation import AssetSimulation
from simulation.MovingAverageSimulationBase import (
    MovingAverageSimulationBase,
)

from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor
from functools import partial
import pandas as pd

INITIAL_CAPITAL = 1000
MOVING_AVERAGE_WINDOW = 50


def _start(
    createConnection: Callable[[], sqlalchemy.engine.Engine], ticker: str
) -> pd.Series:
    engine = createConnection()
    with engine.connect() as db:
        simulationBase = MovingAverageSimulationBase(
            MOVING_AVERAGE_WINDOW, INITIAL_CAPITAL
        )
        simulation = AssetSimulation(db, "2000-01-01", [ticker])
        simulation.setAction(simulationBase.simulate)
        # print(f"Simulating {ticker}")
        simulation.start()

        print(
            f"Ticker {ticker}: ${simulationBase.initialCapital} -> ${simulationBase.cash} => ${simulationBase.cash - simulationBase.initialCapital}"
        )

        return pd.Series(
            data=[
                ticker,
                simulationBase.initialCapital,
                simulationBase.cash,
                simulationBase.cash - simulationBase.initialCapital,
            ],
            index=["ticker", "initialCapital", "endCapital", "delta"],
        )


def start(createConnection: Callable[[], sqlalchemy.engine.Engine]) -> None:
    tickers = None
    with open("../tickers.txt") as f:
        tickers = json.load(f)

    tickers = tickers[:100]
    with ThreadPoolExecutor(10) as executor:
        result = executor.map(partial(_start, createConnection), tickers)
    # result = []
    # for ticker in tickers:
    #     result.append(partial(_start, createConnection)(ticker))

    # for ticker in tickers:
    #     result.append(_start(db, ticker))

    print()
    print("Simulation completed. Results below:")

    final_result = pd.concat(result, axis=1).T
    final_result.to_csv("./ma_results_2.csv")
    sorted_result = final_result.sort_values("delta", ascending=False)
    return sorted_result
