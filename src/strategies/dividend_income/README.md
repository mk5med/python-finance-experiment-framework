Dividends are periodic returns from certain assets. These are often given as a way to entice purchasers to buy the asset as well as reward loyal customers. It is often done when the company has an excess of cash available after their taxes and expenses.

The idea: Create a portfolio of dividend assets that can sustain meaningful passive income.
1. [What conditions are required for this to occur](#conditions-required-for-this-to-occur)
2. [How much capital is required to create this portfolio](#capital-required-to-create-the-portfolio)
3. What is the effectiveness between gained passive income and invested capital
4. What risks are associated with a portfolio of dividend assets
5. How does a portfolio of dividend assets compare to a portfolio of non-dividend assets
6. [Why doesn't everyone create a portfolio of dividend assets](#why-doesnt-everyone-create-a-portfolio-of-dividend-assets)

## Conditions required for this to occur
- Firms must be willing to give dividends -> Firms have excess capital, or the asset has a profit-sharing system
- Firms are allocating a full or subset of their capital to dividends instead of re-investment into themselves
- Taxes on dividend income must be less than 100%
- Assets within the portfolio must distribute dividends -> Assets must be rebalanced when long-term deviations occur
- (Arbitrary) Meaningful passive income occurs when dividend income results in at least 10% of yearly income
- Stable economy ensures minimal to no negative fluctuations to yearly dividend income

## Capital required to create the portfolio
### Core formulas
```java
let d_y = dividend amount per year
let p_i = instantaneous asset price

const incomePerDollar = d_y / p_i
const attractiveness = incomePerDollar
const dividendYield = incomePerDollar
```

Desired income
```java
let desiredIncome = desired yearly income
let qty = quantity of an individual asset

desiredIncome = d_y * qty
const qty = desiredIncome / d_y // Find how many units need to be purchased
const costForDesiredIncome = qty * p_i

// Metric below is equivalent to incomePerDollar
const desiredIncomeToCostFactor = desiredIncome / costForDesiredIncome

desiredIncomeToCostFactor = (d_y * qty) / (qty * p_i) = (d_y) / (p_i) * qty
desiredIncomeToCostFactor = d_y / p_i
desiredIncomeToCostFactor = incomePerDollar 
```

The average dividend yield of all stocks is around 2% to 5%. To receive a yearly passive dividend income of
$1000 with an asset of $1 at 5% dividend yield: a minumum of $20,000 is required. Generally assets
will not cost $1, thus the capital required can extend to the hundred of thousand range.

## Why doesn't everyone create a portfolio of dividend assets
The [capital required](#capital-required-to-create-the-portfolio) to create a dividend portfolio with a reasonable
return is high. Additionally the return on investment for dividends is around 2% to 5% per year, the money can be spent
elsewhere for higher ROI yields. A dividend strategy portfolio is built for long term wealth, where the long term is 10 to 50 years.

Proof:
1. Suppose the desired income per year is $1000
2. Assume a general 2% dividend yield
3. $1000 = 0.02 * x -> $1000 / 0.02 = x -> $50000 = x
4. $1000 = 0.05 * x -> $1000 / 0.05 = x -> $20000 = x
6. $1000 = 0.10 * x -> $1000 / 0.10 = x -> $10000 = x

Investment required is very high and to minimize risk multiple assets will need to be used to diversify the portfolio.
Due to the simplicity of this strategy, even with diversification its likely others are using this and
are invested in the same set of high-dividend yield assets, therefore the risk gained by diversifying may not be as great.

### Combination of yields
1. Asset A1 = 2% yield
2. Asset A2 = 2% yield
3. Asset A3 = 4% yield
4. Net yield (A1, A2, A3, T1, T2, T3, Invested) = (A1, A2, A3) * (T1, T2, T3) * Invested / Invested = (A1, A2, A3) * (T1, T2, T3) = Weighted sum


## Metrics
Historical dividend average price & Volatility
```java
let D = set of all historical dividend price, date groups from the asset over "N"

// Arbitrary value. The idea is to be able to detect signals of change
let shortTermTimeRange = 10

// Measure average price over all time
float averageDividendPrice(n = null) => avg(i.price for i in D or last n elements in D if n is not null)
const longAverageDividendPrice = averageDividendPrice()

// Measure recent average price
const shortAverageDividendPrice = averageDividendPrice(shortTermTimeRange)

// Measure average dividend price change
float dividendVolatility(n = null) => avg(
    D[i].price - D[i-1].price
    for 0 < i < D or last n elements in D if n is not null]
)

// Volatility in the long term
const longDividendVolatility = dividendVolatility()

// Volatility in the short term
const shortDividendVolatility = dividendVolatility(shortTermTimeRange)
```

Historical asset price & volatility
```java
let N = subset of time
let S = set of all historical prices of the asset over "N"

float priceMovingAverage(n = null) => avg([
    i for i in S or last n elements of S if n is not null
  ])

/* Metrics taken from passive reading online */
// A metric for the average price since inception is not used as the asset price changes over the long term. Ideally it should go up, however if it goes down the asset can still be valuable. Hence, an average of all time is not entirely useful right now as it covers a large and unfiltered dataset
// Measures average price over the last 50 days
const priceMovingAverage_50 = priceMovingAverage(50)
// Measures average price over the last 10 days
const priceMovingAverage_10 = priceMovingAverage(10)

float volatilityMovingAverage(n = null) => avg([
    S[i] - S[i-1]
    for 0 < i < S or last n elements of S if n is not null
  ]
])

const volatilityMovingAverage_long = volatilityMovingAverage()
const volatilityMovingAverage_50 = volatilityMovingAverage(50)
const volatilityMovingAverage_10 = volatilityMovingAverage(10)
```

Asset price to price volatility probability table.
i.e: At a given price, what is the probability of a certain price volatility range?
i.e: At a given price, what is the probability of a positive or negative price change?
```java
//
float[] priceToPriceChangeProbability() {
  // resolution: daily, monthly, per transaction
  // per transaction is best for detail but it is noisy
  // daily is less noisy but its difficult to see patterns
}

float[] priceToPriceVolatilityProbability() {
  // Create a line of best fit that estimates the volatility with a price
  // Linear regression can be used for a simple line
  
  // Average daily change
}
```