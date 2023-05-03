import datetime
import typing
import sqlalchemy
import yfinance as yf
from core.lib.Portfolio import Portfolio
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
                sqlalchemy.text(f'select * from "{ticker}" where "Date" = \'{datestr}\'')
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
                    sqlalchemy.text(f'select * from "{ticker}" where "Date" = \'{datestr}\'')
                )
                result = res.fetchone()
                if result is not None:
                    data.append(ticker)

            return data
        except Exception as error:
            if self.dbCon is not None:
                self.dbCon.close()
            raise error

    def getDividendData(self, tickerName: str):
        if tickerName not in TICKERS:  # Cache the record
            TICKERS[tickerName] = yf.Ticker(tickerName)

        ticker = TICKERS[tickerName]
        dividends = None
        if tickerName not in DIVIDENDS:
            # A saved version of dividend information was not found
            dividends = self.__getLatestOrSavedDividends(tickerName, ticker)

            # Cache the dividend information
            DIVIDENDS[tickerName] = dividends
        else:
            # Restore cached dividend information
            dividends = DIVIDENDS[tickerName]

        # Return if there are no dividends for this asset
        if len(dividends) == 0:
            return dividends

        # Filter dividends to dates less than or equal to the current date
        # The simulation cannot look into the future
        return dividends[dividends.keys() <= self.currentDate.isoformat()]

    def __getLatestOrSavedDividends(self, tickerName: str, ticker: yf.Ticker):
        """
        Gets dividends for a Ticker.

        If a ticker has been previously cached to the file system it will read from the saved file.

        If a ticker has not been previously cached it will fetch the latest dividend
        information from yahoo finance and save the results to a file in `../historical_dividends`.
        """
        fName = f"../historical_dividends/{tickerName}-dividend-info.csv"

        # Has the ticker been previously cached
        if not os.path.isfile(fName):

            # Get the latest dividend informatoin
            dividends = ticker.get_dividends()

            # The result can be a dataframe
            if type(dividends) != list:
                dividends.to_csv(fName)
                # Or a list
            else:
                # TODO: Code reuse
                dividends = pd.DataFrame({"Date": [], "Dividends": []})
                dividends.to_csv(
                    fName,
                    index=None,
                )
            # The file was found
        else:
            dividends = pd.read_csv(fName, index_col=0)
            dividends = dividends.squeeze(1)
        return dividends

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
