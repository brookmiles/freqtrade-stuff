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
        dataframe['sell'] = 0
        return dataframe