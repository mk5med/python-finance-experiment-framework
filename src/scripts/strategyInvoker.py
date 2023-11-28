import os
import sys

from experiments.ExperimentManager import ExperimentManager

# Fix dependency resolution when invoking the script directly
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from experiments.strategies.dividend_income import simulate_dividend_income_simulation
from experiments.strategies.crypto import (
    simulate_50_day_moving_average_crypto as simulate_crypto_50_day_moving_average,
)
from experiments.strategies.moving_average import (
    experiment_simulate_50_day_moving_average,
)

experimentManager = ExperimentManager()
experimentManager.registerExperiment(
    "experiments.strategies.moving_average.experiment_simulate_50_day_moving_average"
)

# experimentManager.registerExperiment(
#     "experiments.strategies.crypto.simulate_day_50_moving_average"
# )


def run_all_strategies():
    experimentManager.runAll()
    experimentManager.visualiseAll()
