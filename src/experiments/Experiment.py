import pandas as pd
from typing import Callable
import sqlalchemy
import time
import hashlib


class Experiment:
    def __init__(
        self,
        *,
        experimentID=None,
        experimentName: str,
        experimentDescription: str,
        shouldCache: bool = True,
    ):
        self.experimentID = experimentID
        self.experimentName = experimentName
        self.experimentDescription = experimentDescription
        self.__layer_data = None
        self.__layer_simulation = None
        self.__layer_visualisation = None
        self.results = None
        self.shouldCache = shouldCache

    def setData(self, dataSource: sqlalchemy.engine.Engine) -> None:
        self.__layer_data = dataSource

    def setSimulation(
        self,
        simulation: Callable[[Callable[[], sqlalchemy.engine.Engine]], pd.DataFrame],
    ) -> None:
        self.__layer_simulation = simulation

    def setVisualisation(self, visualisation: Callable[[pd.DataFrame], None]):
        self.__layer_visualisation = visualisation

    def runExperiment(self):
        # Start the timer
        start = time.time()

        # Print a header
        print(f"{'-' * 5} Experiment: {self.experimentName} {'-' * 5}")
        print(self.experimentDescription)
        print("-" * 10)

        result = self.__layer_simulation(self.__layer_data)

        # End the timer
        end = time.time()
        print(f"Duration: {end-start:.03f}s")

        result["strategyName"] = self.experimentName
        result["duration"] = end - start

        self.results = result
        return result

    def visualise(self):
        return self.__layer_visualisation(self.results)
