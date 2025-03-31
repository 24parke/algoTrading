import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import yfinance as yf
import backtrader as bt

stocks = ["COST"]
cerebro = bt.Cerebro()


data = yf.download(stocks, period = "max", interval = "1d", group_by = "tickers")



data['50_SMA'] = data["COST"]['Close'].rolling(window = 30).mean()
data['5_SMA'] = data["COST"]['Close'].rolling(window = 5).mean()
# print(data['Close'])



class a(bt.strategy):
    def __init__(self):
        self.slow = data['50_SMA']
        self.fast = data['5_SMA']
        self.order = None

    def next(self):
        if self.fast > self.slow:
            cash = self.broker.getcash()
            price = self.dta.close[0]
            size = cash/price
            self.order = self.buy(size=size)


data = data.dropna()
cerebro.addstrategy(a)
cerebro.adddata(data)
cerebro.broker.setcash(10000)
cerebro.run()
cerebro.plot()