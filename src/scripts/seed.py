import os
import sys

# Fix dependency resolution when invoking the script directly
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from concurrent.futures import ThreadPoolExecutor
from functools import partial
import json
import pandas as pd
import sqlalchemy

import yfinance as yf


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
            data = pd.read_csv(f"./historical_data/{ticker}.csv")
            data.to_sql(ticker, db)
    except Exception as e:
        print("Fail", e)
        ...


def __collect(tickerPath: str) -> None:
    tickers = None
    print("Collecting most recent data")
    with open(tickerPath) as tickerINode:
        tickers = json.load(tickerINode)

    tickersLen = len(tickers)

    for index, ticker in enumerate(tickers):
        print(f"Downloading {ticker} ({index}/{tickersLen})")
        tickerDownloadDataframe = yf.download(ticker)
        tickerDownloadDataframe.to_csv(f"./historical_data/{ticker}.csv")


def __save(tickerPath: str) -> None:
    print("Seeding database")

    engine = createConnection()
    with open(tickerPath) as f:
        tickers = json.load(f)
        with ThreadPoolExecutor(1) as executor:
            result = executor.map(partial(_start, engine), tickers)


def seed(tickerPath: str) -> None:
    __collect(tickerPath)
    __save(tickerPath)
