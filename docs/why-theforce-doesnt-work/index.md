# TheForce strategy doesn't work

TheForce gets amazing backtest results, but doesn't work live.

The crazy backtest profits are only seen when using `signalperiod=1` with `ta.MACD(dataframe,12,26,1)`

If we switch the MACD implementation from ta-lib, to qtpylib, most of the profits go away:

```
        # MACD (Magic Profits)
        macd = ta.MACD(dataframe,12,26,1)
        dataframe['macd'] = macd['macd']
        dataframe['macdsignal'] = macd['macdsignal']
        dataframe['macdhist'] = macd['macdhist']
```

```
        # MACD (No Magic Profts)
        macd = qtpylib.macd(dataframe['close'],12,26,1)
        dataframe['macd'] = macd['macd']
        dataframe['macdsignal'] = macd['signal']
        dataframe['macdhist'] = macd['histogram']
```

```
================================================================ STRATEGY SUMMARY ===============================================================
|        Strategy |   Buys |   Avg Profit % |   Cum Profit % |   Tot Profit USD |   Tot Profit % |   Avg Duration |   Wins |   Draws |   Losses |
|-----------------+--------+----------------+----------------+------------------+----------------+----------------+--------+---------+----------|
|      TheForceV7 |   1872 |           0.88 |        1641.61 |        24501.162 |        2450.12 |        0:56:00 |   1297 |       0 |      575 |
| TheForceV7_test |   1853 |           0.11 |         209.05 |          506.040 |          50.60 |        0:32:00 |    706 |       0 |     1147 |
=================================================================================================================================================
```

# Why?

What seems to be happening is that ta-lib is, for some reason, cheating by looking into the future by 2 candles when `signalperiod=1`.

This is an overlay of each implementation using `signalperiod=2`, the results quickly converg and overlap each other.

![20210329-172506-msedge](https://user-images.githubusercontent.com/323682/112810586-22f71d80-90b6-11eb-8aa1-0602cbd40731.png)

This is an overlay of each implementation using `signalperiod=1`, the ta-lib version is looking into the future by two candles.  You can see that the ta-lib signal line is two candles "early", predicting the future price movement.

![20210329-172602-msedge](https://user-images.githubusercontent.com/323682/112810643-31ddd000-90b6-11eb-889b-333de04f596a.png)

Just double checking, here is each implementation using `signalperiod=1`, but the ta-lib version has been shifted forward by two candles using `.shift(2)`.  The macd line is now two candles "late", and the signal line once again lines up with the qtpylib implementation.

![20210329-172608-msedge](https://user-images.githubusercontent.com/323682/112810651-34d8c080-90b6-11eb-8b5e-6814345269dd.png)

Sadly TheForce is looking into the future to predict the direction of price movement, which can't happen during live or dry-run, unless you are an _actual Jedi_.
