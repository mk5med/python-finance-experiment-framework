import typing
from experiments.Experiment import Experiment
import hashlib
import importlib
import traceback
import os
import os.path
import pandas as pd


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

        self.experimentIds.add(experiment.experimentID)
        self.experiments.append((experiment, module.__file__))

    def __cacheWrapper(self, experiment: Experiment, experimentPath: str):
        # Skip caching
        if experiment.shouldCache:
            return experiment.runExperiment()

        newFileHash: str = ""

        # Compute the hash of the experiment file
        with open(experimentPath, "rb") as file:
            newFileHash = hashlib.md5(file.read()).digest().hex()

        cacheName = f".cache/experiment-{experiment.experimentID}-{newFileHash}"

        # If the file exists
        if os.path.isfile(cacheName):
            # Restore the cache
            result = pd.read_pickle(cacheName)

        else:
            # Run the experiment
            result = experiment.runExperiment()

            # Save to cache
            result.to_pickle(cacheName)

        return result

    def runAll(self):
        for (experiment, experimentPath) in self.experiments:
            try:
                result = self.__cacheWrapper(experiment, experimentPath)

            except Exception as error:
                print(f"Failed to run experiment {experiment.experimentID}")
                traceback.print_exception(error)
