import os
import sys

from experiments.ExperimentManager import ExperimentManager

# Fix dependency resolution when invoking the script directly
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from concurrent.futures import ThreadPoolExecutor
from functools import partial
from sys import argv
from typing import Callable
from experiments.strategies.dividend_income import simulate_dividend_income_simulation
from experiments.strategies.crypto import (
    simulate_50_day_moving_average_crypto as simulate_crypto_50_day_moving_average,
)
from experiments.strategies.moving_average import experiment_simulate_50_day_moving_average
import json
import pandas as pd
import sqlite3
import psycopg2
import sqlalchemy
import time
import logging


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


def _start(engine: sqlalchemy.engine.Engine, ticker: str) -> None:
    try:
        print(f"Processing {ticker}")
        with engine.connect() as db:
            data = pd.read_csv(f"../historical_data/{ticker}.csv")
            data.to_sql(ticker, db)
    except Exception as e:
        print("Fail", e)
        ...


def seed() -> None:
    print("Seeding database")

    engine = createConnection()
    with open("../tickers.txt") as f:
        tickers = json.load(f)
        with ThreadPoolExecutor(1) as executor:
            result = executor.map(partial(_start, engine), tickers)


experimentManager = ExperimentManager()
experimentManager.registerExperiment(
    "experiments.strategies.moving_average.simulate_50_day_moving_average"
)

# experimentManager.registerExperiment(
#     "experiments.strategies.crypto.simulate_day_50_moving_average"
# )


def run_all_strategies():
    experimentManager.runAll()
