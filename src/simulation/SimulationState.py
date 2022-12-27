import datetime
import sqlite3
import sqlalchemy
import yfinance as yf
from lib.Portfolio import Portfolio

TICKERS = {}


class SimulationState:
    """
    Contains the immutable state of a simulation at a moment in time
    """

    def __init__(self, dbCon: sqlalchemy.engine.Connection, currentDate: str):
        self.currentDate = datetime.datetime.fromisoformat(currentDate)
        self.dbCon = dbCon
        self.portfolio = None
        self._cash = 0

    def setPortfolio(self, portfolio: Portfolio):
        self.portfolio = portfolio
        ...

    def getTickerPrice(self, ticker: str):
        datestr = str(self.currentDate.date())
        cursor = None
        try:
            cursor = self.dbCon
            res = cursor.execute(
                f'select * from "{ticker}" where "Date" = \'{datestr}\''
            )

            # index, date, open, high, low, close, adj close, volume
            return res.fetchone()
        except Exception as error:
            if cursor is not None:
                cursor.close()
            raise error

    def getDividendData(self, ticker: str):
        if ticker not in TICKERS:  # Cache the record
            TICKERS[ticker] = yf.Ticker(ticker)
        t = TICKERS[ticker]
        dividends = t.get_dividends()
        return dividends[dividends.keys() <= self.currentDate.isoformat()]

    def incrementDate(self):
        self.currentDate += datetime.timedelta(days=1)
        if self.currentDate > datetime.datetime.now():
            raise Exception(
                f"Time out of bounds: {self.currentDate} > {datetime.datetime.now()}"
            )

    def getCash(self):
        return self._cash

    def setCash(self, cash: float):
        self._cash = cash
