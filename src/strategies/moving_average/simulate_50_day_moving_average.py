import json

from simulation.AssetSimulation import AssetSimulation
from strategies.moving_average.MovingAverageSimulationBase import (
    MovingAverageSimulationBase,
)

from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor
from functools import partial

INITIAL_CAPITAL = 1000
MOVING_AVERAGE_WINDOW = 50


def _start(db, ticker):
    simulationBase = MovingAverageSimulationBase(MOVING_AVERAGE_WINDOW, INITIAL_CAPITAL)
    simulation = AssetSimulation(db, "2000-01-01", [ticker])
    simulation.setAction(simulationBase.simulate)
    print(f"Simulating {ticker}")
    simulation.start()
    print(
        f"Ticker {ticker}: ${simulationBase.initialCapital} -> ${simulationBase.cash} => ${simulationBase.cash - simulationBase.initialCapital}"
    )


def start(db):
    tickers = None
    with open("../tickers.txt") as f:
        tickers = json.load(f)
    
    with ThreadPoolExecutor(10) as executor:
        result = executor.map(partial(_start, db), tickers)


    for i in result:
        print(i)
