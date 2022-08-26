import sqlite3
from typing import List
import typing
from simulation.SimulationState import SimulationState

ActionCallbackTypeDef = typing.Callable[
    [typing.Callable[[], None], SimulationState, List[str]], None
]


class AssetSimulation:
    def __init__(
        self, db: sqlite3.Connection, startTime, tickers=None, historicalDataINode=None
    ):
        # Load all historical data for the tickers
        # To be memory efficient this should be loaded into a database that is optimised for searching by date
        self.actionCallback: typing.Union[ActionCallbackTypeDef, None] = None
        if historicalDataINode is not None:
            raise Exception(
                "Deprecated: Parsing a json file is outside of the scope for the simulator"
            )

        elif tickers is not None:
            self.tickers = tickers
        else:
            raise Exception("tickers or historicalDataINode must be passed")
        self.simulationState = SimulationState(db, startTime)
        self.running = None

    def setAction(
        self,
        actionCallback: ActionCallbackTypeDef,
    ):
        self.actionCallback = actionCallback

    def nextDay(self):
        self.simulationState.incrementDate()

    def stop(self):
        self.running = False

    def start(self):
        if self.actionCallback is None:
            raise "actionCallback cannot be null"
        # Should ideally support displaying visuals with plotly

        self.running = True

        # TODO: Stop execution when there is no more new data available
        while self.running == True:
            self.actionCallback(self.stop, self.simulationState, self.tickers)
            try:
                self.nextDay()
            except:
                self.stop()
        ...
