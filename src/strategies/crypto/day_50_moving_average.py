from lib.sharegroups import ShareGroups
from lib.tools.movingAverage import MovingAverage
from simulation import SimulationState
from simulation import AssetSimulation

movingAverage = MovingAverage(10)
portfolio = ShareGroups()
cash = 1000
lastAction = 0


def simulate(stopCallback, simulationState: SimulationState, tickers):
    global cash
    global lastAction
    price = simulationState.getTickerPrice("TRL.TO")

    # Skip this entry
    # Cases:
    # - No more data
    # - No data for the current simulation date
    if price == None:
        return

    (index, date, openPrice, high, low, closePrice, adjClose, volume) = price
    adjustedPrice = (openPrice + closePrice) / 2
    historicalAveragePrice = movingAverage.average()

    movingAverage.addData(adjustedPrice)
    if historicalAveragePrice == -1:
        # No average available
        return

    if adjustedPrice > historicalAveragePrice:
        ...
        if lastAction == -1:
            return

        ableToBuy = cash / adjustedPrice
        if ableToBuy == 0:
            return
        # Buy
        cost = portfolio.buy((adjustedPrice, ableToBuy))
        print(f"{simulationState.currentDate}: Buying {ableToBuy} for ${adjustedPrice * ableToBuy} @ {adjustedPrice}")
        cash -= cost
        lastAction = -1
    else:

        # Able to sell
        if portfolio.ownedStocks() == 0:
            return
        portfolio.sunkCosts()
        (profit, shareGroups) = portfolio.maximumProfitAtPrice(adjustedPrice)

        # Reason to sell
        if profit == 0:
            return

        transaction = (
            adjustedPrice,
            sum([i[1] for i in shareGroups]),
        )

        cost = portfolio.sell(transaction, shareGroups)
        cash += cost

        print(f"{simulationState.currentDate}: Sold at ${adjustedPrice}. Current cash", "${:,.2f}".format(cash))
        lastAction = 1


def start(db):
    simulation = AssetSimulation(db, "2001-01-01", tickers=["BTC-CAD"])
    simulation.setAction(simulate)
    simulation.start()
    print("Status", "${:,.2f}".format(cash))
