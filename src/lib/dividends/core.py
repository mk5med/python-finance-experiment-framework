def incomePerDollar(yearlyUnitDividendIncome: float, instantAssetPrice: float):
    return yearlyUnitDividendIncome / instantAssetPrice


def dividendIncomeToYearlyIncome(dividendIncome: float, paymentsPerYear: int):
    """
    dividendIncome - The dividend received per payment
    paymentsPerYear - The number of times the dividend is paid per year
    """
    return dividendIncome * paymentsPerYear
