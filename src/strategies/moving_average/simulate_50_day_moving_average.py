import json
from typing import Callable, List

import sqlalchemy

from simulation.MarketSimulation import MarketSimulation
from strategies.moving_average.MovingAverageSimulation import (
    MovingAverageSimulation,
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
        simulationBase = MovingAverageSimulation(MOVING_AVERAGE_WINDOW, INITIAL_CAPITAL)
        simulation = MarketSimulation(db, "2000-01-01", [ticker])
        simulation.setAction(simulationBase.simulate)
        simulation.start()  # Run the simulation

        # Print the results
        print(
            f"Ticker {ticker}: ${simulationBase.initialCapital} -> ${simulationBase.cash} => ${simulationBase.cash - simulationBase.initialCapital}"
        )

        # Return a summary of the results
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
    with open("./tickers.txt") as f:
        tickers = json.load(f)

    tickers = tickers[:100]

    # BUG: Not the executor is not thread safe
    with ThreadPoolExecutor(1) as executor:
        result = executor.map(partial(_start, createConnection), tickers)
    # result = []
    # for ticker in tickers:
    #     result.append(partial(_start, createConnection)(ticker))

    # for ticker in tickers:
    #     result.append(_start(db, ticker))

    print()
    print("Simulation completed. Results below:")
    # Concat all the results and transpose the result
    final_result = pd.concat(result, axis=1).T

    # Save the results to a CSV
    final_result.to_csv("./ma_results_2.csv")

    # Sort the final summary
    sorted_result = final_result.sort_values("delta", ascending=False)
    return sorted_result
