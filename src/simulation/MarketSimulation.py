import sqlite3
from typing import List
import typing
from simulation.SimulationState import SimulationState
from simulation.MarketSimulationEventBase import MarketSimulationEvent
import sqlalchemy

ActionCallbackTypeDef = typing.Callable[
    [typing.Callable[[], None], SimulationState, List[str]], None
]


class MarketSimulation:
    """
    Controller and executor of simulations.

    Responsible for:
     - Invoking the simulation callback
     - Updating the simulation state
    """

    def __init__(
        self,
        db: sqlalchemy.engine.Connection,
        startTime: str,
        tickers: typing.List[str],
    ):
        # Load all historical data for the tickers
        # To be memory efficient this should be loaded into a database that is optimised for searching by date
        self.actionCallback: typing.Union[
            ActionCallbackTypeDef, None
        ] = lambda _1, _2, _3: None
        self.tickers = tickers
        self.simulationState = SimulationState(db, startTime, self.tickers)
        self.running = False
        self._events: typing.List[MarketSimulationEvent] = []

    def setAction(
        self,
        actionCallback: ActionCallbackTypeDef,
    ) -> None:
        self.actionCallback = actionCallback

    def nextDay(self) -> None:
        # Loop through all events at the end of the day
        for event in self._events:
            event.event(self.stop, self.simulationState, self.tickers)

        self.simulationState.incrementDate()

    def stop(self) -> None:
        self.running = False

    def start(self) -> None:
        if self.actionCallback is None:
            raise Exception("actionCallback cannot be null")
        # Should ideally support displaying visuals with plotly

        self.running = True

        # TODO: Stop execution when there is no more new data available
        while self.running == True:
            self.actionCallback(self.stop, self.simulationState, self.tickers)
            try:
                self.nextDay()
            except Exception as error:
                print(error)
                self.stop()

    def registerEvent(self, event: MarketSimulationEvent):
        """
        Add a new event
        """
        self._events.append(event)
        return self
