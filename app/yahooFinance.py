# -*- coding: utf-8 -*-
"""
Created on Fri Nov 27 04:23:20 2020

@author: Atishay
"""

import yfinance as yf
import time
import datetime as dt
import os
import pandas as pd

# We need to change this, as currently it is running in a local directory
os.chdir("F:\\Trading") 

def getCSVName(symbol, renewRequired, shift = 0):
    if renewRequired:
        curDateTime = dt.datetime.today()
        if curDateTime.hour < 18:
            curDateTime -= dt.timedelta(days=1)
        today = curDateTime - dt.timedelta(days=shift)
        day = today.strftime("%A")
        if(day=="Saturday"):
            today -= dt.timedelta(days=1)
        if(day=="Sunday"):
            today -= dt.timedelta(days=2)
        dateTimeStr = today.strftime("%Y%m%d")
        return symbol + "." + dateTimeStr + ".csv"
    else:
        return symbol + ".csv"

def getFileData(stockPath):
    df = pd.read_csv(stockPath)
    df.set_index("Date", inplace=True)
    return df

"""
There’re some limitations by making the call to Yahoo Finance API:
Using the Public API, you are limited to 2,000 requests per hour per IP.
Or up to a total of 48,000 requests a day.
Please use time.sleep(1) to avoid your IP getting blocked.
"""
def getYahooFinanceData(symbol,period,adjust=False):
    ticker = yf.Ticker(symbol)
    time.sleep(1)
    hist = ticker.history(period=period,auto_adjust=adjust,back_adjust=adjust)
    time.sleep(1)
    return hist

def getHistoricPricing(sym, renewRequired):
    symbolNSE = sym
    symbolBSE = sym
    if sym != "^NSEI":
        symbolNSE += ".NS"
        symbolBSE += ".BO"
    stockPath = "data//stocks//" + getCSVName(sym, renewRequired)
    if os.path.exists(stockPath):
        print("Data present, fetching data from ", stockPath," for ", sym)
        hist = getFileData(stockPath)
    else:
        print("Creating new connection for ", sym ," ETA 5s...")
        hist = getYahooFinanceData(symbolNSE,"max")
        if len(hist) == 0:
            hist = getYahooFinanceData(symbolBSE,"max")
        columnNames = hist.columns
        # print(columnNames)
        hist.columns = [sym+"_"+columnNames[i] for i in range(len(columnNames))]
        hist.to_csv(stockPath)
    return hist

def autoRefresh(curPortfolioSym, oldPortfolioSym, mySym):
    hist = getHistoricPricing("^NSEI", True)[["^NSEI_Close"]]
    for symbol in curPortfolioSym:
        hist = hist.join(getHistoricPricing(symbol, True)[[symbol+"_Close"]])
    for symbol in oldPortfolioSym:
        hist = hist.join(getHistoricPricing(symbol, False)[[symbol+"_Close"]])
    for symbol in mySym:
        hist = hist.join(getHistoricPricing(symbol, True)[[symbol+"_Close"]])
    hist = hist.ffill(axis = 0)
    hist = hist.bfill(axis = 0)
    return hist
