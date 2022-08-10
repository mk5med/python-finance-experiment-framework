def yearlyDividendIncome(yearlyUnitDividendIncome: float, qty: int):
    return yearlyUnitDividendIncome * qty


def quantityForYearlyDividendIncome(
    yearlyIncome: float, yearlyUnitDividendIncome: float
):
    return yearlyIncome / yearlyUnitDividendIncome


def costForIncome(
    yearlyDividendIncome: float,
    yearlyUnitDividendIncome: float,
    instantAssetPrice: float,
):
    qty = quantityForYearlyDividendIncome(
        yearlyDividendIncome, yearlyUnitDividendIncome
    )
    return qty * instantAssetPrice
