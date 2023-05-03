import typing
from experiments.Experiment import Experiment
import hashlib
import importlib
import traceback
import os
import os.path
import pandas as pd
import glob
from matplotlib import pyplot as plt
import plotly
import plotly.express
import plotly.subplots

BASE_CACHE_NAME = ".cache/experiment"


class ExperimentManager:
    def __init__(self) -> None:
        self.experiments: typing.List[typing.Tuple[Experiment, str]] = []
        self.experimentIds: set = set()

        # Set up the cache directory
        if not os.path.isdir(".cache"):
            os.mkdir(".cache")
        pass

    def registerExperiment(self, pathToExperiment: str):
        module = importlib.import_module(pathToExperiment)
        experiment: Experiment = module.experiment
        if experiment.experimentID in self.experimentIds:
            raise Exception(f"Duplicate ID '{experiment.experimentID}'")
        print(experiment.__layer_simulation)
        raise "ERROR"
        self.experimentIds.add(experiment.experimentID)
        self.experiments.append((experiment, module.__file__))

    def __cacheWrapper(self, experiment: Experiment, experimentPath: str):
        # Skip caching
        if not experiment.shouldCache:
            return experiment.runExperiment()

        newFileHash: str = ""

        # Compute the hash of the experiment file
        with open(experimentPath, "rb") as file:
            newFileHash = hashlib.md5(file.read()).digest().hex()

        cacheName = "-".join([BASE_CACHE_NAME, experiment.experimentID, newFileHash])

        # If the file exists
        if os.path.isfile(cacheName):
            # Restore the cache
            result = pd.read_pickle(cacheName)

        else:
            # Run the experiment
            result = experiment.runExperiment()

            # Remove the old cache if it exists
            for cachedFile in glob.glob(
                "-".join([BASE_CACHE_NAME, experiment.experimentID, "*"])
            ):
                os.remove(cachedFile)

            # Save to cache
            result.to_pickle(cacheName)

        return result

    def __printSummary(
        self, experimentStatus: typing.List[typing.Tuple[Experiment, bool]]
    ):
        print("-" * 10)
        print("Experiment summary")
        for (experiment, status) in experimentStatus:
            statusIcon = "✅" if status else "❌"
            print(f"\t{statusIcon} {experiment.experimentID}")

    def runAll(self):
        experimentStatus: typing.List[typing.Tuple[Experiment, bool]] = []
        for (experiment, experimentPath) in self.experiments:
            try:
                result = self.__cacheWrapper(experiment, experimentPath)
                std = result["profit"].std()
                result = result[result["profit"] < std]

                fig = plotly.express.line(
                    result,
                    x="triggered",
                    y="profit",
                    color="ticker",
                )
                fig.show()

                # plt.legend(loc='upper right')
                
                experimentStatus.append((experiment, True))
            except Exception as error:
                print(f"Failed to run experiment {experiment.experimentID}")
                traceback.print_exception(error)
                experimentStatus.append((experiment, False))

        self.__printSummary(experimentStatus)
