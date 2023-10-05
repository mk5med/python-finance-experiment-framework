import typing
from experiments.Experiment import Experiment
import hashlib
import importlib
import traceback
import os
import os.path
import pandas as pd
import glob

BASE_CACHE_NAME = ".cache/experiment"


class ExperimentManager:
    """
    Holds a register of all experiments
    - Invokes all experiments
    - Visualises all experiments
    """

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
        if not experiment.shouldCache:
            return experiment.runExperiment()

        cacheName = "-".join(
            [BASE_CACHE_NAME, experiment.experimentID, experiment.experimentCacheNonce]
        )

        # If the file exists
        if os.path.isfile(cacheName):
            # Restore the cache
            result = pd.read_pickle(cacheName)
            experiment.results = result

        # The file does not exist
        else:
            # Run the experiment
            result = experiment.runExperiment()

            # Remove the old cache if it exists
            for cachedFile in glob.glob(
                "-".join([BASE_CACHE_NAME, experiment.experimentID, "*"])
            ):
                # os.remove(cachedFile)
                ...

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
        """
        Run all registered experiments
        """

        # Store experiment status (failed or complete) in an array
        experimentStatus: typing.List[typing.Tuple[Experiment, bool]] = []

        # Iterate through all experiments
        for (experiment, experimentPath) in self.experiments:
            # Try running the experiment
            try:
                result = self.__cacheWrapper(experiment, experimentPath)
                experimentStatus.append((experiment, True))

            # Log the failed attempt
            except Exception as error:
                print(f"Failed to run experiment {experiment.experimentID}")
                traceback.print_exception(error)
                experimentStatus.append((experiment, False))

        self.__printSummary(experimentStatus)

    def visualiseAll(self):
        for (experiment, experimentPath) in self.experiments:
            experiment.visualise()
