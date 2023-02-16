import datetime
import typing
import sqlalchemy
import yfinance as yf
from lib.Portfolio import Portfolio
import os
import pandas as pd

TICKERS = {}
DIVIDENDS = {}


class SimulationState:
    """
    Contains the immutable state of a simulation at a moment in time
    """

    def __init__(
        self,
        dbCon: sqlalchemy.engine.Connection,
        currentDate: str,
        tickers: typing.List[str],
    ):
        self.currentDate = datetime.datetime.fromisoformat(currentDate)
        self.dbCon = dbCon
        self._portfolio = None
        self._cash = 0
        self._tickers = tickers

    def setPortfolio(self, portfolio: Portfolio):
        self._portfolio = portfolio

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

    def getAvailableTickers(self) -> typing.List[str]:
        datestr = str(self.currentDate.date())
        try:
            data: typing.List[str] = []
            for ticker in self._tickers:
                res = self.dbCon.execute(
                    f'select * from "{ticker}" where "Date" = \'{datestr}\''
                )
                result = res.fetchone()
                if result is not None:
                    data.append(ticker)

            return data
        except Exception as error:
            if self.dbCon is not None:
                self.dbCon.close()
            raise error

    def getDividendData(self, ticker: str):
        if ticker not in TICKERS:  # Cache the record
            TICKERS[ticker] = yf.Ticker(ticker)

        t = TICKERS[ticker]
        dividends = None
        if ticker not in DIVIDENDS:
            # Cache the dividend information to memory
            if not os.path.isfile(
                f"../historical_dividends/{ticker}-dividend-info.csv"
            ):
                dividends = t.get_dividends()
                if type(dividends) != list:
                    dividends.to_csv(
                        f"../historical_dividends/{ticker}-dividend-info.csv"
                    )
                else:
                    # TODO: Code reuse
                    dividends = pd.DataFrame({"Date": [], "Dividends": []})
                    dividends.to_csv(
                        f"../historical_dividends/{ticker}-dividend-info.csv",
                        index=None,
                    )

            else:
                dividends = pd.read_csv(
                    f"../historical_dividends/{ticker}-dividend-info.csv", index_col=0
                )
                dividends = dividends.squeeze(1)
            DIVIDENDS[ticker] = dividends
        else:
            # Restore cached dividend information
            dividends = DIVIDENDS[ticker]

        if len(dividends) == 0:
            return dividends
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

    def buy(self, ticker: str, qty: float):
        assert self._portfolio is not None
        ref = self._portfolio.getTickerRef(ticker)
        data = self.getTickerPrice(ticker)
        if data is None:
            raise Exception(
                f"Asset is delisted or is not available at this time {self.currentDate}"
            )

        # Calculate the average price
        price = data[2] + data[5] / 2
        ref.transactions.buy((price, qty))
        self._cash -= price * qty

    def sell(self, ticker: str, qty: float):
        assert self._portfolio is not None
        ref = self._portfolio.getTickerRef(ticker)
        data = self.getTickerPrice(ticker)
        raise NotImplementedError("Not implemented yet")
