# -*- coding: utf-8 -*-
"""
Created on Fri Sep 14 23:22:08 2018

@author: Media Service
"""


import pandas as pd
import datetime
import pandas_datareader.data as web
import matplotlib.pyplot as plt
from matplotlib import style
import quandl


# Not necessary, I just do this so I do not show my API key.

df = quandl.get("FMAC/HPI_TX", authtoken= "1KPAsT__H3CRmAJDn4Xk")

#print(df.head())

# buscando estados
fiddy_states = pd.read_html('https://simple.wikipedia.org/wiki/List_of_U.S._states')
# lista de DataFrames
print(fiddy_states )

for abbv in fiddy_states[0][1][1:]:
    print(abbv)
# construyendo el ticker
    for abbv in fiddy_states[0][0][1:]:
    #print(abbv)
    print("FMAC/HPI_"+str(abbv))
    
    
    
    
    
    
    