def yearlyDividendIncome(yearlyUnitDividendIncome: float, qty: int) -> float:
    return yearlyUnitDividendIncome * qty


def quantityForYearlyDividendIncome(
    yearlyIncome: float, yearlyUnitDividendIncome: float
) -> float:
    return yearlyIncome / yearlyUnitDividendIncome


def costForIncome(
    yearlyDividendIncome: float,
    yearlyUnitDividendIncome: float,
    instantAssetPrice: float,
) -> float:
    qty = quantityForYearlyDividendIncome(
        yearlyDividendIncome, yearlyUnitDividendIncome
    )
    return qty * instantAssetPrice
