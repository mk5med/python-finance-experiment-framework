import typing
import sqlalchemy
from lib.Portfolio import Portfolio
from simulation import SimulationState, MarketSimulation
from functools import partial

from simulation.events import DividendEvent


def simulate(
    stopSimulation: typing.Callable[[], None],
    simulationState: SimulationState,
    tickers: typing.List[str],
) -> None:
    ...


class SimpleDividendIncomeOptions:
    def __init__(self, *, startYear: str, minDividendYield: float):
        self.startYear = startYear
        self.minDividendYield = minDividendYield


class SimpleDividendIncomeSimulationResult:
    def __init__(
        self, *, endCash: float, initialisationCost: float, portfolio: Portfolio
    ):
        self.profit = endCash
        self.sunkCost = initialisationCost
        self.roi = self.profit / self.sunkCost
        self.portfolio = portfolio

    def __str__(self) -> str:
        return f"{self.__class__.__name__}(profit={self.profit}, sunkCost={self.sunkCost}, roi={self.roi}, tickers={self.portfolio.tickers.keys()})"


def builder(options: SimpleDividendIncomeOptions):
    return partial(__start, options)


def __start(
    options: SimpleDividendIncomeOptions,
    createConnection: typing.Callable[[], sqlalchemy.engine.Engine],
):
    """
    # Simple Dividend Income
    1) Create a portfolio with the best dividend return
    2) Evaluate the portfolio periodically and rebalance as needed
      A dividend portfolio will be rebalanced every time the price changes
      this can happen either per minute or per day
      we will use per day to speed up the simulation.
      To account for fluctuations we will use the average between the open and close
    """
    import json

    engine = createConnection()

    with engine.connect() as db:
        with open("../tickers.txt") as f:
            # Load all the tickers
            allTickers = json.load(f)
            portfolio = Portfolio()
            simulation = MarketSimulation(db, options.startYear, tickers=allTickers)
            simulation.simulationState.setPortfolio(portfolio=portfolio)
            simulation.setAction(simulate)

            # Listen for dividend events
            simulation.registerEvent(DividendEvent.DividendEvent())

            print("Initialising experiment portfolio")
            __initPortfolio(options, simulation)
            assetCount = len([i for i in portfolio.tickers])
            if assetCount == 0:
                raise Exception("No assets found")
            print(f"Found {assetCount} assets")
            print("Started market simulation")

            # Get the amount paid to initialize the portfolio
            initialisationCost = abs(simulation.simulationState.getCash())

            # Reset cash to 0
            simulation.simulationState.setCash(0)

            simulation.start()
            endCash = simulation.simulationState.getCash()

            return SimpleDividendIncomeSimulationResult(
                endCash=endCash,
                initialisationCost=initialisationCost,
                portfolio=portfolio,
            )


def __initPortfolio(
    options: SimpleDividendIncomeOptions, simulation: MarketSimulation
) -> MarketSimulation:
    tickers = simulation.simulationState.getAvailableTickers()

    for ticker in tickers:
        dData = simulation.simulationState.getDividendData(ticker)

        # Skip if there is no dividend data
        if len(dData) == 0:
            continue

        data = simulation.simulationState.getTickerPrice(ticker)
        price = data[5]
        lastDividend = dData[-1]

        dividendYield = lastDividend / price
        # If the last yield is greater than or equal to the DIVIDEND_YIELD
        if dividendYield >= options.minDividendYield:
            simulation.simulationState.buy(ticker, 1)

    return simulation


def start(createConnection: typing.Callable[[], sqlalchemy.engine.Engine]) -> None:
    return builder(
        SimpleDividendIncomeOptions(startYear="2000-01-07", minDividendYield=0.10)
    )(createConnection)
