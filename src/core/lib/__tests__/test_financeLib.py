import sys, os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from lib.financeLib import transaction_sell
import pytest


class Test_transaction_sell:
    def test_simple_sell(self) -> None:
        transactions = [(1, 1)]
        with pytest.raises(AssertionError) as exc_info:
            transaction_sell((1, -1), transactions)
        assert len(transactions) == 1

    def test_lazy_sell(self) -> None:
        transactions = [(1, 1)]
        transaction_sell((1, 1), transactions)
        assert len(transactions) == 2
        assert transactions[1] == (1, -1)
