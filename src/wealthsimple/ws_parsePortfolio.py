import json
from pydoc import classname
from bs4 import BeautifulSoup
import re

ignoreKeys = ["Withdrawal", "Funds transferred in", "Funds transferred out", "Deposit"]


def getTicker(elem):
    return elem.find(class_="sc-ihNHHr jjDDSu").text


def getTransactionDetails(elem):
    if elem.find(attrs={"data-qa": "wstrade-info-item-Quantity"}) == None:
        return [None, elem.find(class_="sc-ihNHHr gqesxw").text]
    match = re.match(
        "^(\d+\.?\d*) shares? x \$([\d,]+\.\d+)",
        elem.find(attrs={"data-qa": "wstrade-info-item-Quantity"}).text,
    )
    out = list(match.groups()[::-1])
    out[0] = out[0].replace(",", "")

    return [tuple([float(i) for i in out]), None]


def ws_portfolio():
    with open("../raw/portfolio.json", "r") as file:
        parsedJSON = json.load(file)
        keys = list(filter(lambda key: key not in ignoreKeys, parsedJSON.keys()))

        portfolio = {}
        for i in keys:
            transactions = parsedJSON[i]
            for transaction in transactions:
                html = BeautifulSoup(transaction, features="lxml")
                ticker = getTicker(html)
                [transactionEntry, _] = getTransactionDetails(html)
                if ticker not in portfolio:
                    portfolio[ticker] = []
                if transactionEntry is None:
                    continue
                portfolio[ticker].append(transactionEntry)
        return portfolio


if __name__ == "__main__":
    print(ws_portfolio())
