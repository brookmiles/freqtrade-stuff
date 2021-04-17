# Recommendations

I do not recommend you run any of these strategies live. 

Be sure to understand what they do and the risks involved if you decide to do so.

# FAQ

## Ichimoku Slow

My live configs are what you see [here ../](../)

### What is your stake size / max trades?

I find max open trades values between 3-5 to have the best results in backtesting.

Too few and you risk having them all filled with weak sideways trades; too many and you risk frequently idle slots, and smaller profits on winning trades.

### What are your pairlist settings?

For VolumePairList limits, I find 10-25 have the best results in backtesting.  Too few and you risk excluding reasonably strong pairs that are currently climbing in activity; too many and you will find your trade slots filled with weak trades from low volume pairs that are noisy and have weak trends.

The quality and type of pairs available on each exchange varies considerably, so do your own backtests to compare how different options compare.

Use `test-pairlist` to generate the current results of your pairlist, and backtest over some recent timeframes.  Running a backtest on data from years ago, using a pairlist generated today is less realistic, as the pairlist at the time would likely have been very different.
