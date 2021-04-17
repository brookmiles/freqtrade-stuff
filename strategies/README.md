# Recommendations

I do not recommend you run any of these strategies live. 

Be sure to understand what they do and the risks involved if you decide to do so.

# FAQ

## Ichimoku Slow

My live configs are what you see [here ../](../../../)

### What is your stake size / max trades?

I find max open trades values between 3-5 to have the best results in backtesting.

Too few and you risk having them all filled with weak sideways trades; too many and you risk frequently idle slots, and smaller profits on winning trades.

### What are your pairlist settings?

For VolumePairList limits, I find 10-25 have the best results in backtesting.  Too few and you risk excluding reasonably strong pairs that are currently climbing in activity; too many and you will find your trade slots filled with weak trades from low volume pairs that are noisy and have weak trends.

The quality and type of pairs available on each exchange varies considerably, so do your own backtests to see how different options compare.

Use `test-pairlist` to generate the current results of your pairlist, and backtest over some recent timeframes.  Running a backtest on data from years ago, using a pairlist generated today is less realistic, as the pairlist at the time would likely have been very different.

### I've been running Ichimoku Slow for 1-2 days and it's losing money, what gives?

I am not an expert, I do not recommend you run any of my strategies live, and I make no claims as to their expected future performance or suitability for any purpose. 

As always, trade only what you are willing to lose.

There are also a few important design considerations to consider:

- As the name implies, Ichimoku Slow does not trade frequently and attempts to follow trends from beginning to end, often for many days.

The biggest wins will come from following strong uptrends for multiple days.  If there have been no strong multi-day uptrends in the time since the strategy was launched, it's not likely to have made any profit.

If the market enters a long sideways or down period, there will be no uptrends to follow.  The strategy may not trade for days at a time, or it may repeatedly buy into upswings that only last a very short time before failing.

- Ichimoku Slow will buy into ongoing trends.  

This is by design, as the expectation is that you will have fewer trade slots available than whitelisted pairs.  During bull markets there will likely be more trending pairs than you have trade slots. When a trade slot opens up, it will buy into another pair that is trending.

An alternative would be to only buy into trends at the beginning of the trend, however in backtesting this has shown to be far less profitable due to the very high chance that the buy signal will be missed, because there were no available trade slots to open a new trade.  The beginning of the trend may also be missed if the pair did not have sufficient volume at the start of the trend to be active in the pairlist until after the start of the trend.

### Why doesn't Ichimoku Slow use a stoploss?

Since Ichimoku Slow buys into ongoing trends, hitting a stoploss would likely result in the strategy re-buying into the same trend on the next candle.

### When will Ichimoku Slow sell?

Ichimoku Slow will sell when the trend has come to an end as determined by the SSL Channel indicator crossing over from high to low.

### Why does Ichimoku Slow sell once the price falls and not at the peak?

I am not an expert, and I welcome any contributions which improve the sell criteria.
