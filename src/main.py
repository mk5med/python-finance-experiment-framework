from lib.sharegroups import ShareGroups
from wealthsimple.ws_parsePortfolio import ws_portfolio

BTC_TRANSACTIONS = [
    (38358.27, 0.002607),
    (53648.07, 0.000466),
    (70621.47, 0.000354),
    (70721.36, 0.000707),
    (47543.58, 0.001893),
    (45330.92, 0.001103),
    (80808.08, 0.000198),
    (76288.66, 0.00097),
    (75872.53, 0.001318),
    (63572.79, 0.001573),
    (45330.92, 0.001103),
]

# GFL.TO
# AR.TO
# TYMB.V


def print_futureReturns(
    sg: ShareGroups, CUR_PRICE: float, newPrice: float, desiredReturn: float
):
    print("Mapping possible future returns")
    print(f"\tNew price: ${newPrice}")
    requiredTransaction = sg.transactionForReturnAtPrice(
        CUR_PRICE, newPrice, desiredReturn
    )
    print(f"\tMAX profit at new price: ${sg.maximumProfitAtPrice(newPrice)}")
    print(
        f"\tOptimal transaction to get ${desiredReturn} at the new price => {requiredTransaction} => ${requiredTransaction[0] * requiredTransaction[1]}"
    )


if __name__ == "__main__":
    print("importing yf")
    import yfinance as yf

    print("imported yf")
    PORTFOLIO = ws_portfolio()
    TRANSACTIONS = []
    # TRANSACTIONS = PORTFOLIO['BITF']
    # TRANSACTIONS = BTC_TRANSACTIONS

    # print(PORTFOLIO)
    sg = ShareGroups.fromSimpleChain(TRANSACTIONS)
    # sg.sell((25456.5, 0.005586), [(53648.07, 0.000466),
    #   (70621.47, 0.000354),
    #   (70721.36, 0.000707),
    #   (80808.08, 0.000198),
    #   (76288.66, 0.00097),
    #   (75872.53, 0.001318),
    #   (63572.79, 0.001573)])

    ticker = yf.Ticker("FM.TO")
    ticker = yf.Ticker("BTC-CAD")
    # ticker = yf.Ticker("BITF.TO")
    # ticker = yf.Ticker("ME.TO")
    ticker = yf.Ticker("WBE.V")

    CUR_PRICE = ticker.history(period="1d")["Close"][0]

    print(f"Current price: ${CUR_PRICE}")
    print("Sunk costs:", sg.sunkCosts())
    print(f"Current return: ${sg.netAssetReturn(CUR_PRICE)}")
    print(f"Price needed to break even: ${sg.priceForReturn(0)}")
    print(f"Price needed to earn $1: ${sg.priceForReturn(1)}")
    print(f"Price needed to earn $10: ${sg.priceForReturn(10)}")

    print_futureReturns(sg, CUR_PRICE, CUR_PRICE * 2.01, 1000)
