import json
from typing import Callable, List

import sqlalchemy
from core.helpers.prettyFromToProfitPrint import printFromToProfit

from core.simulation.MarketSimulation import MarketSimulation
from experiments.strategies.moving_average.MovingAverageSimulation import (
    MovingAverageSimulation,
)

from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor
from functools import partial
import pandas as pd


def analyseResults(ticker: str, result: MovingAverageSimulation):
    """
    Analyse the results of a moving average simulation and create an aggregate final result
    """
    
    # How much yield does a 50 day moving average give?
    net_yield = (result.cash) / result.initialCapital
    transactions_length = len(result.portfolio.shareGroupTransactionChain)
    results = []
    for i in result.events:
        time_held = i.dateSold - i.dateBought
        investment_cost = i.priceBought
        profit = i.priceSold - i.priceBought
        instant_yield = profit / investment_cost
        results.append(
            pd.Series(
                data=[
                    ticker,
                    i.dateSold,
                    time_held,
                    i.priceBought,
                    i.priceSold,
                    profit,
                    instant_yield,
                ],
                index=[
                    "ticker",
                    "triggered",
                    "time_held",
                    "buyPrice",
                    "sellPrice",
                    "profit",
                    "instant_yield",
                ],
            )
        )

    return results
