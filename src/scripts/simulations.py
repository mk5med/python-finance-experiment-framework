import os
import sys

# Fix dependency resolution when invoking the script directly
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from concurrent.futures import ThreadPoolExecutor
from functools import partial
from sys import argv
from typing import Callable
from strategies.dividend_income import simulate_dividend_income_simulation
from strategies.crypto import (
    simulate_day_50_moving_average as simulate_crypto_50_day_moving_average,
)
from strategies.moving_average import simulate_50_day_moving_average
import json
import pandas as pd
import sqlite3
import psycopg2
import sqlalchemy
import time


def __createPostgresConnection() -> sqlalchemy.engine.Engine:
    USERNAME = "postgres"
    PASSWORD = "example"
    HOST = "127.0.0.1"

    engine = sqlalchemy.create_engine(
        f"postgresql+psycopg2://{USERNAME}:{PASSWORD}@{HOST}",
        pool_recycle=3600,
    )
    return engine


def createConnection() -> sqlalchemy.engine.Engine:
    # __createPostgresConnection()

    engine = sqlalchemy.create_engine(
        f"sqlite+pysqlite:///simulationDB.sqlite3",
        connect_args={"check_same_thread": False},
    )
    return engine


engine = createConnection()


def _start(ticker: str) -> None:
    try:
        print(f"Processing {ticker}")
        with engine.connect() as db:
            data = pd.read_csv(f"./historical_data/{ticker}.csv")
            data.to_sql(ticker, db)
    except Exception as e:
        print("Fail", e)
        ...


def seed() -> None:
    print("Seeding database")
    with open("./tickers.txt") as f:
        tickers = json.load(f)
        with ThreadPoolExecutor(1) as executor:
            result = executor.map(partial(_start), tickers)

        # for i in result:
        #     print(result)


def run_simulation(
    strategyName: str,
    simulation: Callable[[Callable[[], sqlalchemy.engine.Engine]], pd.DataFrame],
):

    start = time.time()
    result = simulation(createConnection)
    end = time.time()
    print(result)
    print(
        f"This strategy ranges from ${min(result['delta'])} to ${max(result['delta'])} in profit."
    )
    print(f"Duration: {end-start:.03f}s")

    return pd.Series(
        {
            "strategyName": strategyName,
            "duration": end - start,
            "range_min": min(result["delta"]),
            "range_max": max(result["delta"]),
        }
    )


def run_all_simulations():
    # simulate_dividend_income_simulation.start(engine)
    # simulate_crypto_50_day_moving_average.start(engine)
    run_simulation("50-day moving average. CAD", simulate_50_day_moving_average.start)


if __name__ == "__main__":
    if "--seed" in argv:
        seed()
