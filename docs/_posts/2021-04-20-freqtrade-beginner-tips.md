---
layout: post
---

> Hi, I'm new. Do you have any advice for beginners?

I am not an expert, and nothing that follows is financial advice.  These are my opinions based on my experience so far.

# Financial Advice

Trading is risky, and trading crypto is especially risky.  Only trade what you are willing to lose.

* My first priority is preserving my capital.

Crypto trading is not for you.  You may want to look into a balanced ETF portfolio, bonds, GICs, or a high rate savings account.  Speak to a qualified financial advisor.

* I want to make crazy profits, and I'm willing to risk losing everything I've invested for the chance to get them.

Carry on.

# Basics

There are broadly 3 different areas you should become familiar with in order to trade using Freqtrade.

1. General trading terminology, and technical analysis.
2. A baseline of technical skill, and basic programming knowledge. The ability to read and understand Python code.
3. How to use Freqtrade specifically, its features and limitations.

## General Trading

You should have a basic understanding of how trading works in general.  Be sure to understand the terms *market order* and *limit order* and the difference between them, *bid-ask spread*, *volume*, *slippage*, how the *order book* works, *spot* vs. *margin* trading, how a *stop-loss order* works.

All of this information is common to classical trading and crypto trading, search for them on Google or [Investopedia](https://www.investopedia.com/).

Once you've got the basics of trading covered, you'll want to dig deeper into *Technical Analysis*, which involves looking at historical price data and determining patterns which you expect to repeat in the future with enough confidence to inform your trading decisions.  Technical Analysis typically uses *chart patterns* or *technical indicators*.

This is in contrast to *Fundamental Analysis* which focuses on looking at the actual performance or value of companies or assets which are being traded, news stories, public sentiment, etc..

Freqtrade strategies typically focus entirely on Technical Analysis.

- [Guide To Technical Analysis](https://www.investopedia.com/terms/t/technical-analysis-of-stocks-and-trends.asp)

Familiarize yourself with basic indicators such as moving averages, MACD, Bollinger Bands, and RSI.

If your exchange supports paper-trading (simulated, with no real money), then choose a crypto currency to practice trading with.  Set up a chart on your exchange or TradingView that has a few indicators that interest you, and make some paper trades based on them.

Be sure to read not just what the indicators show directly, but about how they are typically used by traders, and for what purpose.  Some monitor trends, some can be used as signals to make a buy or sell, etc...

- [How to Combine Trading Indicators](https://youtu.be/QdbKApfwF-g)

## Programming Skills

I don't recommend using Freqtrade without at least basic understanding of programming fundamentals and the Python language.

Freqtrade does not come with a "default" strategy that makes money.  You must evaluate each strategy that you intend to use to make sure that at a minimum it does something even remotely sensible, and in the worst case is at least not actively malicious.

If you are unable to at least review a strategy in order to spot obvious mistakes or potentially malicious code, then you will be at the mercy of whoever provided the strategy to you.

At a more general level, strategies will perform differently depending on the exchange they are run on, timing, the current market conditions, the trading pairs used, the timeframe used, the specific configuration of your freqtrade bot, and so on.  You may need to make at least basic changes to the strategy code in order to make it more suitable your specific situation.

- [Python For Beginners](https://www.python.org/about/gettingstarted/)

If you aren't comfortable or interested in learning Python basics, then Freqtrade may not be the best fit for you.

## Freqtrade Specifics

A few key points:

- Freqtrade does not automatically make money. There is no "default" strategy that you can turn on to earn a profit.  Strategies are written in Python by you, or shared by other users.
- Making profit trading is challenging, time consuming, and not at all guaranteed. The same goes for automated trading, although ideally it becomes less time consuming when (and if) you find a strategy and configuration that is working for you long term and can be run with minimal active management.

Freqtrade supports spot trading only. You cannot use it to make short trades, to trade using margin, or to trade options contracts or futures.

Freqtrade does not support position stacking.  You cannot use Freqtrade to gradually buy more of a coin.  Once a trade is opened, it has to be sold before another trade can be made for the same coin.

### Getting Started

1. Install Freqtrade using the instructions on the [official website](https://www.freqtrade.io/), either using Docker, or directly on your machine.
1. Grab the free strategies provided in the separate [freqtrade-strategies](https://github.com/freqtrade/freqtrade-strategies) github repository.  Some of the strategies collected under `user_data/strategies/berlinguyinca/` in particular are excellent starting points or references for developing your own strategies, and will often be mentioned by other Freqtrade users.
1. Download the data that you'll need to use for backtesting using the [`download-data`](https://www.freqtrade.io/en/stable/data-download/) command.
1. Refer to the [Configuration](https://www.freqtrade.io/en/stable/configuration/), as it will be necessary to make changes to your configuration in order to get much of anything else done.
1. Start backtesting strategies using the [`backtesting`](https://www.freqtrade.io/en/stable/backtesting/) command.
1. Once you've run a backtest or two, use the [Plotting](https://www.freqtrade.io/en/stable/plotting/) functionality to visualize the results of your backtests.  This can be incredibly helpful in understanding what your strategy is actually doing.  Try out both the `plot-dataframe` and `plot-profit` commands.
1. Before putting real money on the line, or even setting up your exchange keys, choose a strategy to [run in *dry-run* mode](https://www.freqtrade.io/en/stable/configuration/#using-dry-run-mode), which will simulate trades in realtime using public data provided by your exchange.  
1. Set up [Telegram](https://www.freqtrade.io/en/stable/telegram-usage/) to monitor the bot during the dry-run.

Make use of the search function at the top of the [Freqtrade Offical Website](https://www.freqtrade.io/en/stable/) first, whenever you have a question about a specific command, config parameter, or topic.  If you don't find what you're looking for, you can ask for help on [Discord or Slack](https://www.freqtrade.io/en/stable/#help-discord-slack).

