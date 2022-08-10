import datetime
import sqlite3


class SimulationState:
    def __init__(self, dbCon: sqlite3.Connection, currentDate: str):
        self.currentDate = datetime.datetime.fromisoformat(currentDate)
        self.dbCon = dbCon
        ...

    def getTickerPrice(self, ticker: str):
        datestr = str(self.currentDate.date())
        cursor = None
        try:
            cursor = self.dbCon.cursor()
            res = cursor.execute(f"select * from \"{ticker}\" where Date = '{datestr}'")

            # index, date, open, high, low, close, adj close, volume
            return res.fetchone()
        except Exception as e:
            if cursor is not None:
                cursor.close()
            raise e

    def getNextDividendData(self, ticker: str):
        ...

    def incrementDate(self):
        self.currentDate += datetime.timedelta(days=1)
        if self.currentDate > datetime.datetime.now():
            raise Exception(
                f"Time out of bounds: {self.currentDate} > {datetime.datetime.now()}"
            )
