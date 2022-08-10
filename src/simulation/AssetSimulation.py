from io import TextIOWrapper
from typing import List, Tuple
import typing
import json
import pandas as pd
from simulation.SimulationState import SimulationState


class AssetSimulation:
    def __init__(self, db, startTime, tickers=None, historicalDataINode=None):
        # Load all historical data for the tickers
        # To be memory efficient this should be loaded into a database that is optimised for searching by date
        self.actionCallback = None
        if historicalDataINode is not None:
            raise "Deprecated: Parsing a json file is outside of the scope for the simulator"
            self.tickers = json.load(historicalDataINode)
        elif tickers is not None:
            self.tickers = tickers
        else:
            raise Exception("tickers or historicalDataINode must be passed")
        self.simulationState = SimulationState(db, startTime)
        self.running = None

    def setAction(
        self,
        actionCallback: typing.Callable[
            [typing.Callable[[], None], SimulationState, List[str]], None
        ],
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
