---
title: Backtesting Traps
date: 2021-04-12T20:00:00+09:00
layout: post
---

Backtesting is important to understand the performance and behaviour of your strategy, but there are a number of issues which can result in a backtest producing much better results than are likely once the strategy is run live (or dry-run).

This information applies to the Hyperopt feature as well, which processes strategies in the same way as Backtesting.

To start with, make sure to familiarize yourself with the [official documentation on Backtesting](https://www.freqtrade.io/en/stable/backtesting/#assumptions-made-by-backtesting) and it's assumptions.  

## Basics

- The Future Will Be Different From The Past

  Backtesting tests use historical data, so even if your strategy avoids all of the other problems, there's no guarantee that it will succeed in the future, even if it succeeded on past data.

- Trade Timeouts

  When backtesting, all of your trade orders are magically filled at the exact price you wanted.  This doesn't happen in real life, and if you place limit orders, it's likely that some percentage of them go unfilled and time out, causing you to miss entering or exiting a trade.  The likelyhood of this happening depends on the volume of the pair you're trading, when your strategy places orders, whether the market is moving up or down, which side of the bid/ask spread you place your orders on, etc...

- Slippage

  Regardless of which order type you use, the market will continue to move between the time your strategy decides to place and order, and that order actually getting placed, and hopefully filled on the exchange.  Particularly when using market orders, this causes price slippage and it is likely that you will get a somewhat worse price than the moment the strategy decided to place an order.  How much worse will depend on the exact market conditions, spread, volume, the size of your order, price direction, etc...

Refer to [Prices Used For Orders](https://www.freqtrade.io/en/stable/configuration/#prices-used-for-orders) and [Market Order Pricing](https://www.freqtrade.io/en/stable/configuration/#market-order-pricing) in the Configuration documentation for details.



## Reading Future Candles

Something that can be difficult to get used to when backtesting is that signals are generated from the entire time range at one time.  The bot does not start at the first candle and process each candle in order.

`populate_indicators`, `populate_buy_trend`, and `populate_sell_trend` are called once for a given pair, and generate all of the signals for the entire duration.  This means that the "end" of the Dataframe is always the final candle of the backtesting time range, and is not the "most recent" candle as it would be when running live or dry.

When creating the signals for any given candle it is therefor easy to accidentally read from the candles which follow in the Dataframe, effectively "seeing into the future".  When running dry or live, the future is not available.

Read the official documentation on [common mistakes made when developing strategies](https://www.freqtrade.io/en/stable/strategy-customization/#common-mistakes-when-developing-strategies) for details on things to avoid.

## Trailing Stops

> *"i keep tightening trailing stoploss and backtest profits go up. that cant be right."*

One backtesting anomaly that seems to produce incredible, one might even say *unbelieveable*, results is the use of very small trailing stops.

Here's an example strategy that exploits this feature.  It uses no signals, and simply buys on every candle on a 1h timeframe.  Sells happen by reaching minimum ROI of 1%, or by hitting the trailing stoploss of 0.1%.

``` python
from freqtrade.strategy.interface import IStrategy
from typing import Dict, List
from pandas import DataFrame

class Magic_Trailing_Stoploss(IStrategy):

    minimal_roi = { "0": 0.01 }

    stoploss = -0.01
    
    trailing_stop = True
    trailing_stop_positive = 0.001

    timeframe = '1h'

    def populate_indicators(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        return dataframe

    def populate_buy_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        dataframe['buy'] = 1
        return dataframe

    def populate_sell_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        return dataframe
```

Now we backtest...

![20210412-173449-powershell](https://user-images.githubusercontent.com/323682/114368495-6b373500-9bb8-11eb-8cc5-0e8103c31d9a.png)

In only 11 days, we've gone from $2,500 to $65,150, a 2506% profit! Amazing!

Sadly, this strategy will not produce similar results when run live.

First of all, take a look at the Avg. Duration Winners / Losers.  1 minute, and 7 minutes respectively.  When trading hour long candles, this is a sign that you're exploiting the behaviour of backtesting.

Using [`plot-dataframe`](https://www.freqtrade.io/en/latest/plotting/) can further help illustrate what's happening:

![20210412-174319-msedge](https://user-images.githubusercontent.com/323682/114384829-316f2a00-9bca-11eb-99ad-1d834ea87e12.png)

Most of the candles show that the trade opened and close in the same candle, which backtesting will consider to be 0 minutes, or on the very next candle.

### What's Going On?

When backtesting at any timeframe, Freqtrade has only candle data to work with. It doesn't know how the price moved *during the candle*.  With 1m or 5m candles, it's less of a problem (although it still exists), but with longer timeframes, like 1h, 4h, etc... Freqtrade needs to make some major assumptions about the order of events.

As mentioned in the [official documentation on Backtesting](https://www.freqtrade.io/en/stable/backtesting/#assumptions-made-by-backtesting), when Freqtrade calculates trailing stoploss, it first moves the price to the high, moves the trailing stop up to match accordingly, and then moves the price down, possibly triggering the new trailing stop price.

Backtesting with extremely tight trailing stops essentially gives you a perfect candle trade, selling just below the high of the candle, almost every time.

The longer the timeframe you use, the less realistic this is.  With a small trailing stoploss, it's exceptionally unlikely that the price would move directly from open to high without decreasing enough to trigger the stoploss.  If your stoploss is smaller than the spread on the pair you're trading, the stoploss will likely be hit on the next sell trade. The longer the timeframe, the more likely your trailing stop, or even your default stoploss, will be triggered before reaching the high and then falling.

#### ROI

If you have a reasonably tight ROI set, you may see the ROI hit instead of the candle high, but the same trailing stop issue applies.  The longer the candle, the less likely the price will actually reach the ROI before triggering your trailing stop.

### What To Watch Out For

Things to watch out for while you're developing/backtesting your strategy that might be a clue that you're accidentally exploiting this behaviour:

- Average duration of trades is lower than your candle timeframe, maybe only a few minutes when using 1h candles.
- When plotted, trades regularly close on the same candle that they are opened.
- Your trailing stop is lower than, or not much bigger than the spread on the pairs you're trading.  Typical spreads range from 0.1% to 0.5% on high volume coins, and are often much higher on low volume coins.
- Profits keep increasing as you decrease the size of your trailing stop.

## Trailing Stop Workaround

One solution you can use to ensure that you are seeing more realistic backtest results is to backtest your 1h strategy at 5m or 1m, using an informative pair at 1h to generate trade signals.  The signals will operate on the same 1h timeframe that live does, and running the strategy using 5m or 1m candle data will simulate price movement during that 1h, providing more realistic trailing stoploss and ROI behaviour.

Unfortunately this will be slower than backtesting at 1h, and it complicates the code somewhat.  But if you plan on using a trailing stoploss or ROI, you probably want to know that your backtest results are not complete lies.

Here is a simple strategy that uses a simple EMA crossover to generate buy signals: [EMA_Trailing_Stoploss](EMA_Trailing_Stoploss.py)


``` python
from freqtrade.strategy import IStrategy
from typing import Dict, List
from pandas import DataFrame
import talib.abstract as ta
import freqtrade.vendor.qtpylib.indicators as qtpylib

class EMA_Trailing_Stoploss(IStrategy):

    minimal_roi = { "0": 0.01 }

    stoploss = -0.01
    
    trailing_stop = True
    trailing_stop_positive = 0.001

    timeframe = '1h'

    def populate_indicators(self, dataframe: DataFrame, metadata: dict) -> DataFrame:

        dataframe['ema3'] = ta.EMA(dataframe, timeperiod=3)
        dataframe['ema5'] = ta.EMA(dataframe, timeperiod=5)
        dataframe['go_long'] = qtpylib.crossed_above(dataframe['ema3'], dataframe['ema5']).astype('int')

        return dataframe

    def populate_buy_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        dataframe.loc[
            qtpylib.crossed_above(dataframe['go_long'], 0)
        ,
        'buy'] = 1

        return dataframe

    def populate_sell_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        return dataframe
```

Backtesting shows a very respectable 11% profit, but this is an illusion:

![20210412-215010](https://user-images.githubusercontent.com/323682/114396964-25d72f80-9bd9-11eb-82ae-5397efc87e05.png)

And the same strategy after converting it to be backtested at 5m or 1m: [EMA_Trailing_Stoploss_LessMagic](EMA_Trailing_Stoploss_LessMagic.py)

- change `timeframe` to 5m and add `informative_timeframe`
- move indicators from `populate_indicators` to a new function called `do_indicators`
- `populate_indicators` checks timeframe and run mode, and runs `do_indicators` directly when live, or runs it using the 1h informative pairs and then merges the results back into the main dataframe when backtesting.
- put all of your signal creation in `do_indicators`, and only read buy/sell signals from `populate_buy_trend` / `populate_sell_trend`

``` python
from freqtrade.strategy import IStrategy, merge_informative_pair
from typing import Dict, List
from pandas import DataFrame
import talib.abstract as ta
import freqtrade.vendor.qtpylib.indicators as qtpylib
from freqtrade.exchange import timeframe_to_minutes

class EMA_Trailing_Stoploss_LessMagic(IStrategy):

    minimal_roi = { "0": 0.01 }

    stoploss = -0.01
    
    trailing_stop = True
    trailing_stop_positive = 0.001

    timeframe = '5m'
    informative_timeframe = '1h'

    def informative_pairs(self):
        pairs = self.dp.current_whitelist()
        informative_pairs = [(pair, self.informative_timeframe) for pair in pairs]
        return informative_pairs

    def do_indicators(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        dataframe['ema3'] = ta.EMA(dataframe, timeperiod=3)
        dataframe['ema5'] = ta.EMA(dataframe, timeperiod=5)
        dataframe['go_long'] = qtpylib.crossed_above(dataframe['ema3'], dataframe['ema5']).astype('int')
        return dataframe

    def populate_indicators(self, dataframe: DataFrame, metadata: dict) -> DataFrame:

        if self.config['runmode'].value in ('backtest', 'hyperopt'):
            assert (timeframe_to_minutes(self.timeframe) <= 5), "Backtest this strategy in 5m or 1m timeframe."

        if self.timeframe == self.informative_timeframe:
            dataframe = self.do_indicators(dataframe, metadata)
        else:
            if not self.dp:
                return dataframe

            informative = self.dp.get_pair_dataframe(pair=metadata['pair'], timeframe=self.informative_timeframe)

            informative = self.do_indicators(informative.copy(), metadata)

            dataframe = merge_informative_pair(dataframe, informative, self.timeframe, self.informative_timeframe, ffill=True)
            skip_columns = [(s + "_" + self.informative_timeframe) for s in ['date', 'open', 'high', 'low', 'close', 'volume']]
            dataframe.rename(columns=lambda s: s.replace("_{}".format(self.informative_timeframe), "") if (not s in skip_columns) else s, inplace=True)

        return dataframe

    def populate_buy_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        dataframe.loc[
            qtpylib.crossed_above(dataframe['go_long'], 0)
        ,
        'buy'] = 1

        return dataframe

    def populate_sell_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        return dataframe
```

Backtesting now shows all of the profits have vanished, this is much closer to what would happen live, and will be even lower once spread, slippage, unfilled orders, etc... are accounted for.

![20210412-215036](https://user-images.githubusercontent.com/323682/114397037-37b8d280-9bd9-11eb-9dfa-c6170cd4b8bc.png)
