import sys, os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from lib.ShareGroupTransactionChain import ShareGroupTransactionChain


def test_call():
    s = ShareGroupTransactionChain()
    s.buy((1, 1))
    assert s.simpleTransactions.transactions == [(1, 1)]


def test_convertSimpleTransaction():
    transactions = [(1, 1), (4, 1), (3, -1)]
    sg = ShareGroupTransactionChain.fromSimpleChain(transactions)
    assert sg != None
    assert len(sg.simpleTransactions.transactions) == 3
