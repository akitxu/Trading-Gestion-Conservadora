# -*- coding: utf-8 -*-
"""
Created on Fri Sep 14 19:02:24 2018

@author: Media Service
"""

import pandas as pd
import datetime
import pandas_datareader.data as web

#start = datetime.datetime(2010, 1, 1) #  # necesita importar datetime
#end = datetime.datetime.now()
#start = pd.Timestamp("2016/1/1")
#end = pd.Timestamp("2018/1/30") 
#start = "2016-01-01"
#end = "2018-02-05"
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning) 

# Imoprtar cotizaciones de un único valor
df = web.DataReader('MMM', 'yahoo', start, end)

# importar cotizaciones de varios valores
tickers = ["IBE.MC", "R4.MC", "TRUEVALUEFI.BC", "F00000H5PN.BC"]
# Obtener df de cada ticker en un único df, ordenado por ticker y por fechas 
def get(tickers, start, end):
    def data(ticker):
        return web.DataReader(ticker, 'yahoo', start, end)
    datas = map(data, tickers)       
    return pd.concat(datas, keys=tickers, names=['Ticker','Date'])

all_data = get(tickers, start, end)
print (all_data[:3])
print (df.info())