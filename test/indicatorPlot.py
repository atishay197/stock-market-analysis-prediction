#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Feb 12 11:38:51 2020

@author: atishay
"""

import datetime as dt
import os
import sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from yahooFinance import getHistoricPricing

def plotRSI(price,symbol,trimData=False,sd=dt.datetime(2008, 1, 1), ed=dt.datetime(2009,12,31)):
    if trimData:
        price = price[sd:ed]
        # print(price)
    figure, (ax0,ax1) = plt.subplots(2,figsize=(12, 8))
    figure.suptitle("Relative Strength Indicator")
    ax0.plot(price[symbol+"_Close"])
    ax1.plot(price["RSI"],color='k')
    price["RSI70"] = price["RSI"][price["RSI"]>70]
    price["RSI30"] = price["RSI"][price["RSI"]<30]
    legend = ["RSI"]
    if trimData:
        ax1.plot(price["RSI70"],color='springgreen', marker='^')
        ax1.plot(price["RSI30"],color='lightcoral', marker='v')
        legend = ["RSI","OverBought > 70%" ,"OverSold < 30%"]
    else:
        ax1.fill_between(price["RSI70"].index,70, price["RSI70"] ,color='springgreen')
        ax1.fill_between(price["RSI30"].index,30, price["RSI30"],color='lightcoral')
    ax1.axhline(y=70, color='g', linestyle='--')
    ax1.axhline(y=30, color='r', linestyle='--')
    ax1.set_yticks(range(0,110,10))
    ax0.set(xlabel="Date", ylabel="Stock Price")
    # ax0.legend([symbol])
    ax1.set(xlabel="Date", ylabel="RSI")
    ax1.legend(legend)
    ax0.grid()
    ax1.grid()
    figureName = "RelativeStrengthIndicator.png"
    if trimData:
        figureName = "RelativeStrengthIndicator_T.png"    
    figure.savefig(figureName)

def plotBB(price,symbol,trimData=False,sd=dt.datetime(2008, 1, 1), ed=dt.datetime(2009,12,31)):
    if trimData:
        price = price[sd:ed]
        # print(price)
    figure, (ax0,ax1) = plt.subplots(2,figsize=(12, 8))
    figure.suptitle("Bollinger Bands")
    ax0.plot(price[symbol+"_Close"],color='k')
    ax0.plot(price["UBB"],color='g', linestyle='--')
    ax0.plot(price["LBB"],color='r', linestyle='--')
    dateRange = price["UBB"].index
    ax0.fill_between(dateRange,price["UBB"], price["LBB"], alpha=0.2)
    ax0.plot(price["SMA"],color='b')
    ax0.set(xlabel="Date", ylabel="Stock Price")
    ax0.legend(["Closing Price","Upper Bollinger Band","Lower Bollinger Band","Simple Moving Average"])
    
    ax1.plot(price["BBP"],color='blue')
    price["BBP1"] = price["BBP"][price["BBP"]>1]
    price["BBP2"] = price["BBP"][price["BBP"]<-1]
    legend = ["Bollinger Band %"]
    if trimData:
        ax1.plot(price["BBP1"],color='springgreen', marker='^')
        ax1.plot(price["BBP2"],color='lightcoral', marker='v')
        legend = ["Bollinger Band %","Sell Signal","Buy Signal"]
    else:
        ax1.fill_between(price["BBP1"].index,1, price["BBP1"] ,color='springgreen')
        ax1.fill_between(price["BBP2"].index,-1, price["BBP2"],color='lightcoral')
    ax1.axhline(y=1, color='g', linestyle='--')
    ax1.axhline(y=-1, color='r', linestyle='--')
    ax1.set(xlabel="Date", ylabel="Bollinger Band %")
    ax1.legend(legend)    
    
    ax0.grid()
    ax1.grid()
    
    figureName = "BollingerBand.png"
    if trimData:
        figureName = "BollingerBand_T.png"    
    figure.savefig(figureName)

def plotMACD(price,symbol,trimData=False,sd=dt.datetime(2008, 1, 1), ed=dt.datetime(2009,12,31)):
    if trimData:
        price = price[sd:ed]
    figure, (ax0,ax1) = plt.subplots(2,figsize=(12, 8))
    # minMaxList = []
    # minMaxList.append(-1*price["MACD"].min())
    # minMaxList.append(price["MACD"].max())
    # minMaxList.append(-1*price["MACD_EM9"].min())
    # minMaxList.append(price["MACD_EM9"].max())
    # maxRange = int(np.ceil(np.array(minMaxList).max()))
    # print(maxRange)
    positive = price["MACD_HIST"][price["MACD_HIST"]>0]
    negative = price["MACD_HIST"][price["MACD_HIST"]<0]
    
    figure.suptitle("Moving Average Convergence Divergence")
    ax0.plot(price[symbol+"_Close"])
    ax0.plot(price["EM12"])
    ax0.plot(price["EM26"])
    ax1.plot(price["MACD"])
    ax1.plot(price["MACD_EM9"])
    ax1.bar(positive.index,positive, width = 2, color='springgreen')
    ax1.bar(negative.index,negative, width = 2, color='lightcoral')
    ax1.axhline(y=0, color='k', linestyle='-')
    ax0.set(xlabel="Date", ylabel="Stock Price")
    ax0.legend(["Closing Price","12 Day EMA","26 Day EMA"])
    ax1.set(xlabel="Date", ylabel="MACD")
    ax1.legend(["MACD","9 Day EMA of MACD"])    
    ax0.grid()
    ax1.grid()
    # ax1.set_yticks(range(-1*maxRange,maxRange+1,1))
    figure.savefig("MovingAverageConvergenceDivergence.png")



#def callIndicators():
symbol = "RELIANCE.NS"
ticker, hist = getHistoricPricing(symbol, "10y")

rsi = RSI(hist,symbol,14)
plotRSI(rsi,symbol)
plotRSI(rsi,symbol,True,dt.datetime(2020, 1, 1),dt.datetime(2020,12,1))
# print(rsi)

bb = BB(hist,symbol)
plotBB(bb,symbol)
plotBB(bb,symbol,True,dt.datetime(2020, 1, 1),dt.datetime(2020,12,1))
# print(bb)
    
macd = MACD(hist,symbol)
plotMACD(macd,symbol)
plotMACD(macd,symbol,True,dt.datetime(2020, 1, 1),dt.datetime(2020,12,1))

