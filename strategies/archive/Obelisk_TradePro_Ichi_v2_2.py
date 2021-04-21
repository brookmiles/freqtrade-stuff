# --- Do not remove these libs ---
from freqtrade.strategy import IStrategy, merge_informative_pair
from pandas import DataFrame
import talib.abstract as ta
import freqtrade.vendor.qtpylib.indicators as qtpylib

# --------------------------------
import pandas as pd
import numpy as np
import technical.indicators as ftt
from freqtrade.exchange import timeframe_to_minutes

# Obelisk_TradePro_Ichi v2.2 - 2021-04-04
#
# by Obelisk 
# https://github.com/brookmiles/
#
# WARNING
#
# While this strategy is designed to be run at 1h, it should be backtested at 5m (or 1m).
# This is done to avoid misleading results produced using trailing stops and roi values at longer timeframes.
#
# When running at 5m, an informative pair at 1h will be used to generate signals equivalent to running at 1h.
#
# live / dryrun: use 1h
# backtest / hyperopt: use 5m or 1m
#
# WARNING see note on stoploss_on_exchange below
#
# Contributions:
#
# JimmyNixx 
#  - SSL Channel confirmation
#  - ROCR & RMI confirmations
#
#
# Backtested with pairlist generated from:
# "pairlists": [
#     {
#         "method": "VolumePairList",
#         "number_assets": 50,
#         "sort_key": "quoteVolume",
#         "refresh_period": 1800
#     },
#     {"method": "AgeFilter", "min_days_listed": 10},
#     {"method": "PrecisionFilter"},
#     {"method": "PriceFilter", 
#         "low_price_ratio": 0.001,
#         "max_price": 20,
#     },
#     {"method": "SpreadFilter", "max_spread_ratio": 0.002},
#     {
#         "method": "RangeStabilityFilter",
#         "lookback_days": 3,
#         "min_rate_of_change": 0.1,
#         "refresh_period": 1440
#     },
# ],

def SSLChannels(dataframe, length = 7):
    df = dataframe.copy()
    df['ATR'] = ta.ATR(df, timeperiod=14)
    df['smaHigh'] = df['high'].rolling(length).mean() + df['ATR']
    df['smaLow'] = df['low'].rolling(length).mean() - df['ATR']
    df['hlv'] = np.where(df['close'] > df['smaHigh'], 1, np.where(df['close'] < df['smaLow'], -1, np.NAN))
    df['hlv'] = df['hlv'].ffill()
    df['sslDown'] = np.where(df['hlv'] < 0, df['smaHigh'], df['smaLow'])
    df['sslUp'] = np.where(df['hlv'] < 0, df['smaLow'], df['smaHigh'])
    return df['sslDown'], df['sslUp']

class Obelisk_TradePro_Ichi_v2_2(IStrategy):

    # Do not change the timeframe values in this file
    # Use the config file or command line options to select the appropriate timeframe:
    #     5m - BACKTEST or HYPEROPT
    #     1h - LIVE or DRYRUN

    # Backtest or hyperopt at this timeframe
    timeframe = '5m'

    # Generate signals from the 1h timeframe
    # Live or Dry-run at this timeframe
    informative_timeframe = '1h'

    # WARNING
    # ichimoku is a long indicator, if you remove or use a 
    # shorter startup_candle_count your results will be unstable/invalid 
    # for up to a week from the start of your backtest or dry/live run
    # (180 candles = 7.5 days)
    startup_candle_count = 180

    # This strat only uses candle information, so processing between
    # new candles is a waste of resources as nothing will change
    process_only_new_candles = True

    # ROI table:
    minimal_roi = {
        "0": 0.16,
        "40": 0.1,
        "90": 0.035,
        "210": 0
    }

    # I haven't been able to determine a good default stoploss.
    # Select or hyperopt an stoploss that you're happy with, and backtest the result.
    #
    # Do not use stoploss_on_exchange if you leave the stoploss at the default value 
    # or the bot may trigger emergencysell when it fails to place the stoploss.
    #
    # Stoploss:
    stoploss = -0.99

    plot_config = {
        # Main plot indicators (Moving averages, ...)
        'main_plot': {
            'senkou_a': {
                'color': 'green',
                'fill_to': 'senkou_b',
                'fill_label': 'Ichimoku Cloud',
                'fill_color': 'rgba(0,0,0,0.2)',
            },
            # plot senkou_b, too. Not only the area to it.
            'senkou_b': {
                'color': 'red',
            },
            'tenkan_sen': { 'color': 'orange' },
            'kijun_sen': { 'color': 'blue' },

            'chikou_span': { 'color': 'lightgreen' },

            # 'ssl_up': { 'color': 'green' },
            # 'ssl_down': { 'color': 'red' },
        },
        'subplots': {
            "Signals": {
                'go_long': {'color': 'blue'},
                'buy_criteria': {'color': 'green'},
                'sell_criteria': {'color': 'red'},
            },
        }
    }

    def informative_pairs(self):
        pairs = self.dp.current_whitelist()
        informative_pairs = [(pair, self.informative_timeframe) for pair in pairs]
        return informative_pairs

    def do_indicators(self, dataframe: DataFrame, metadata: dict):

        # # Standard Settings
        # displacement = 26
        # ichimoku = ftt.ichimoku(dataframe, 
        #     conversion_line_period=9, 
        #     base_line_periods=26,
        #     laggin_span=52, 
        #     displacement=displacement
        #     )

        # Crypto Settings
        displacement = 30
        ichimoku = ftt.ichimoku(dataframe, 
            conversion_line_period=20, 
            base_line_periods=60,
            laggin_span=120, 
            displacement=displacement
            )

        dataframe['chikou_span'] = ichimoku['chikou_span']

        # cross indicators
        dataframe['tenkan_sen'] = ichimoku['tenkan_sen']
        dataframe['kijun_sen'] = ichimoku['kijun_sen']

        # cloud, green a > b, red a < b
        dataframe['senkou_a'] = ichimoku['senkou_span_a']
        dataframe['senkou_b'] = ichimoku['senkou_span_b']
        dataframe['leading_senkou_span_a'] = ichimoku['leading_senkou_span_a']
        dataframe['leading_senkou_span_b'] = ichimoku['leading_senkou_span_b']
        dataframe['cloud_green'] = ichimoku['cloud_green'] * 1
        dataframe['cloud_red'] = ichimoku['cloud_red'] * -1

        # DANGER ZONE START

        # NOTE: Not actually the future, present data that is normally shifted forward for display as the cloud
        dataframe['future_green'] = (dataframe['leading_senkou_span_a'] > dataframe['leading_senkou_span_b']).astype('int') * 2

        # The chikou_span is shifted into the past, so we need to be careful not to read the
        # current value.  But if we shift it forward again by displacement it should be safe to use.
        # We're effectively "looking back" at where it normally appears on the chart.
        dataframe['chikou_high'] = (
                (dataframe['chikou_span'] > dataframe['senkou_a']) &
                (dataframe['chikou_span'] > dataframe['senkou_b'])
            ).shift(displacement).fillna(0).astype('int')

        # DANGER ZONE END

        ssl_down, ssl_up = SSLChannels(dataframe, 10)
        dataframe['ssl_down'] = ssl_down
        dataframe['ssl_up'] = ssl_up
        dataframe['ssl_high'] = (ssl_up > ssl_down).astype('int') * 3

        dataframe['rocr'] = ta.ROCR(dataframe, timeperiod=28)
        dataframe['rmi-fast'] = ftt.RMI(dataframe, length=9, mom=3)

        dataframe['go_long'] = (
                (dataframe['tenkan_sen'] > dataframe['kijun_sen']) &
                (dataframe['close'] > dataframe['senkou_a']) &
                (dataframe['close'] > dataframe['senkou_b']) &
                (dataframe['future_green'] > 0) &
                (dataframe['chikou_high'] > 0) &
                (dataframe['ssl_high'] > 0) &
                (dataframe['rocr'] > dataframe['rocr'].shift()) &
                (dataframe['rmi-fast'] > dataframe['rmi-fast'].shift(2))
                ).astype('int') * 4

        return dataframe

    def populate_indicators(self, dataframe: DataFrame, metadata: dict) -> DataFrame:

        if self.config['runmode'].value in ('backtest', 'hyperopt'):
            assert (timeframe_to_minutes(self.timeframe) <= 5), "Backtest this strategy in 5m or 1m timeframe. Read comments for details."

        if self.timeframe == self.informative_timeframe:
            dataframe = self.do_indicators(dataframe, metadata)
        else:
            if not self.dp:
                return dataframe

            informative = self.dp.get_pair_dataframe(pair=metadata['pair'], timeframe=self.informative_timeframe)

            informative = self.do_indicators(informative.copy(), metadata)

            dataframe = merge_informative_pair(dataframe, informative, self.timeframe, self.informative_timeframe, ffill=True)
            # don't overwrite the base dataframe's HLCV information
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

        dataframe.loc[
                (dataframe['ssl_high'] == 0)
                &
                (
                    (dataframe['tenkan_sen'] < dataframe['kijun_sen'])
                    |
                    (dataframe['close'] < dataframe['kijun_sen'])
                )
        ,
        'sell'] = 1

        return dataframe

