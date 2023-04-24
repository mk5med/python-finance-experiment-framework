import pandas as pd
from typing import Callable
import sqlalchemy
import time
import matplotlib.pyplot as plt


class ExperimentManager:
    def __init__(
        self, *, experimentID=None, experimentName: str, experimentDescription: str
    ):
        self.experimentID = experimentID
        self.experimentName = experimentName
        self.experimentDescription = experimentDescription
        self.__layer_data = None
        self.__layer_simulation = None
        self.results = None

    def setData(self, dataSource: sqlalchemy.engine.Engine) -> "ExperimentManager":
        self.__layer_data = dataSource
        return self

    def setSimulation(
        self,
        simulation: Callable[[Callable[[], sqlalchemy.engine.Engine]], pd.DataFrame],
    ) -> "ExperimentManager":
        self.__layer_simulation = simulation
        return self

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
