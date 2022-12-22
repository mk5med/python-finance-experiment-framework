from lib.ShareGroups import ShareGroups


def test_call():
    s = ShareGroups()
    s.buy((1, 1))
    assert s.simpleTransactions.transactions == [(1, 1)]


def test_convertSimpleTransaction():
    transactions = [(1, 1), (4, 1), (3, -1)]
    sg = ShareGroups.fromSimpleChain(transactions)
    assert sg != None
    assert len(sg.simpleTransactions.transactions) == 3