import asyncio
# from finta import TA
import time
# from finta.utils import resample
import sched, time
import math
from decimal import *
from datetime import datetime
import pandas as pd
import asyncio
import ccxt.async_support as ccxt
import nest_asyncio
# import pandas_ta as pTA
import os
from finta import TA

nest_asyncio.apply()
# __import__('IPython').embed()
PAIRS = ["ADA/USDT"]
# TIMEFRAME = os.environ["timeframe"]
TIMEFRAME = '1m'
# HIGHER_TIMEFRAME = os.environ["higher_timeframe"]
HIGHER_TIMEFRAME = '5m'
LEVERAGE = 1

async def fetch_candles(pair, binance):
    candles = await binance.fetch_ohlcv(pair, TIMEFRAME)
    # h_candles = await binance.fetch_ohlcv(pair, HIGHER_TIMEFRAME)

    columns = ["date", "open", "high", "low", "close", "volume"]
    df = pd.DataFrame.from_records(candles, index=["date"], columns=columns)
    df.index = pd.to_datetime(df.index, unit="ms")

    # h_df = pd.DataFrame.from_records(h_candles, index=["date"], columns=columns)
    # h_df.index = pd.to_datetime(df.index, unit="ms")
    return df, h_df

async def loop():
    binance = ccxt.binance(
        {
            "apiKey": "",
            "secret": "",
            "enableRateLimit": True,
            "options": {"defaultType": "future"},
        }
    )
    markets = await binance.load_markets()
    for pair in PAIRS:
        print(f"----- NEW PAIR -----")
        print(f"Searching: {pair}")
        if await buy_signal(pair, binance):
            print("Buy it")
            # notification.send_this(f"Buy {pair}")
        elif await sell_signal(pair, binance):
            print("Sell it")
            # notification.send_this(f"Sell {pair}")

    await binance.close()

    return {"Success": True}


async def sell_signal(pair, binance):
    df, h_df = await fetch_candles(pair, binance)
    df = apply_indicators(df)
    h_df = apply_indicators(h_df)
    df.dropna()
    # supertrend3 = pTA.supertrend(df['high'], df['low'], df['close'], 10, 3)
    # supertrend2 = pTA.supertrend(df['high'], df['low'], df['close'], 11, 2)
    # supertrend1 = pTA.supertrend(df['high'], df['low'], df['close'], 12, 1)
    if (
        # supertrend2['SUPERTd_11_2.0'][-1] == -1
        # and supertrend1['SUPERTd_12_1.0'][-1] == -1
        df['close'][-1] < df["EMA200"][-1]
        and df['STOCHK'][-1] < df['STOCHD'][-1]
        and df['STOCHK'][-2] >= df['STOCHD'][-2]
        and h_df['MACD'][-1] < h_df['MACDS'][-1]
    ):
        return True
    return False



async def buy_signal(pair, binance):
    df, h_df = await fetch_candles(pair, binance)
    df = apply_indicators(df)
    h_df = apply_indicators(h_df)

    df.dropna()
    # supertrend3 = pTA.supertrend(df['high'], df['low'], df['close'], 10, 3)
    # supertrend2 = pTA.supertrend(df['high'], df['low'], df['close'], 11, 2)
    # supertrend1 = pTA.supertrend(df['high'], df['low'], df['close'], 12, 1)
    # print(supertrend3['SUPERTd_10_3.0'][-1])
    # print(supertrend2['SUPERTd_11_2.0'][-1])
    # print(supertrend1['SUPERTd_12_1.0'][-1])
    print(h_df['MACD'][-1])
    print(h_df['MACDS'][-1])
    if (
        # supertrend2['SUPERTd_11_2.0'][-1] == 1
        # and supertrend1['SUPERTd_12_1.0'][-1] == 1
        df['close'][-1] > df["EMA200"][-1]
        and df['STOCHK'][-1] > df['STOCHD'][-1]
        and df['STOCHK'][-2] <= df['STOCHD'][-2]
        and h_df['MACD'][-1] > h_df['MACDS'][-1]
    ):
        return True
    return False


def apply_indicators(df):
    
    df["EMA200"] = TA.EMA(df, 200)
    df["EMA50"] = TA.EMA(df, 50)
    df["EMA21"] = TA.EMA(df, 21)
    df["EMA5"] = TA.EMA(df, 5)
    df["BOLL"] = TA.BOLL
    # df["RSI"] = TA.RSI(df)
    # df['STOCHK'] = TA.STOCH(df)
    # df['STOCHD'] = TA.STOCHD(df)
    # df[['MACD','MACDS']] = TA.MACD(df)
    return df


# def s_strategy(df):

#     if (
#         df['RSI'][-2] >= 50,
#         df['RSI'][-1] < 50,
#         df['EMA200'][-1] > df['close'][-1]
#     ):
#         return True,
#     return False


#     stop_loss_params = {"stopPrice": sl, "closePosition": True}
#     order2 = await exchange.create_order(
#         pair, "stop_market", "sell", amount, None, stop_loss_params
#     )
#     take_profit_params = {"stopPrice": tp, "closePosition": True}
#     order3 = await exchange.create_order(
#         pair, "TAKE_PROFIT_MARKET", "sell", amount, None, take_profit_params
#     )


def handler(event, context):
    asyncio.run(loop())

# async def order(pair, exchange):

#     balance = await exchange.fetch_balance()
#     print(balance)
#     cost = 0
#     cost = RISK * float(balance["BUSD"]["free"])
#     print(cost)
#     ticker = await exchange.fetch_ticker(pair)

#     price = ticker["last"]
#     amount = cost / price * LEVERAGE
#     sl = price * 0.995
#     tp = price * 1.01

#     params = {
#         # "test": True,  # test if it's valid, but don't actually place it
#     }

#     order = await exchange.create_order(
#         symbol=pair, type="market", side="buy", amount=amount, price=None, params=params
#     )
#     print(order)

#     order1_price = order["price"]
#     if order1_price is None:
#         order1_price = order["average"]
#     if order1_price is None:
#         cumulative_quote = float(order["info"]["cumQuote"])
#         executed_quantity = float(order["info"]["executedQty"])
#         order1_price = cumulative_quote / executed_quantity

#     stop_price = order1_price * 0.99


