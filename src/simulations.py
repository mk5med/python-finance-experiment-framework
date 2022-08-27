from concurrent.futures import ThreadPoolExecutor
from functools import partial
from sys import argv
from strategies.dividend_income import simulate_dividend_income_simulation
from strategies.crypto import (
    simulate_day_50_moving_average as crypto_simulate_day_50_moving_average,
)
from strategies.moving_average import simulate_50_day_moving_average
import json
import pandas as pd
import sqlite3
import psycopg2
import sqlalchemy


def __createPostgresConnection():
    USERNAME = "postgres"
    PASSWORD = "example"
    HOST = "127.0.0.1"

    engine = sqlalchemy.create_engine(
        f"postgresql+psycopg2://{USERNAME}:{PASSWORD}@{HOST}",
        pool_recycle=3600,
    )
    return engine


def createConnection():
    # __createPostgresConnection()

    engine = sqlalchemy.create_engine(
        f"sqlite+pysqlite:///simulationDB.sqlite3",
        connect_args={"check_same_thread": False},
    )
    return engine


# db = sqlite3.connect("simulationDB.sqlite3", check_same_thread=False)
engine = createConnection()


def _start(ticker):
    try:
        print(f"Processing {ticker}")
        with engine.connect() as db:
            data = pd.read_csv(f"../historical_data/{ticker}.csv")
            data.to_sql(ticker, db)
    except Exception as e:
        print("Fail", e)
        ...


def seed():
    with open("../tickers.txt") as f:
        tickers = json.load(f)
        with ThreadPoolExecutor(100) as executor:
            result = executor.map(partial(_start), tickers)

        # for i in result:
        #     print(result)


if __name__ == "__main__":
    if "--seed" in argv:
        seed()

    with engine.connect() as db:
        # dividend_income_simulation.start(db)
        # crypto_simulate_day_50_moving_average.start(db)
        simulate_50_day_moving_average.start(db)
        ...
