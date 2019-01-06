# -*- coding: utf-8 -*-
"""
Created on Fri Sep 14 20:53:03 2018

@author: Media Service
"""

import pandas as pd
import datetime
import pandas_datareader.data as web
import matplotlib.pyplot as plt
from matplotlib import style

web_stats = {'Day':[1,2,3,4,5,6],
             'Visitors':[43,34,65,56,29,76],
             'Bounce Rate':[65,67,78,65,45,52]}

# convertimos el diccionario en un DataFrame
df = pd.DataFrame(web_stats)




import matplotlib.pyplot as plt
from matplotlib import style
df.set_index('Day', inplace=True)
style.use('fivethirtyeight')

#print(df['Visitors'])

df.plot()
plt.show()



df = pd.read_csv('ZILLOW-Z77006_ZRISFRR.csv')
df.set_index('Date', inplace = True)
df.to_csv('newcsv2.csv')

df = pd.read_csv('newcsv2.csv')
df = pd.read_csv('newcsv2.csv', index_col=0)
# cambiar nombre de una columna
df.columns = ['House_Prices']
df.to_csv('newcsv3.csv')

df.to_csv('newcsv.csv', header=False)
#print(df[:3])

df = pd.read_csv('newcsv4.csv', names = ['Date','House_Price'], index_col=0)

df.to_html('example.html')
#print(df.head()) 
 
df = pd.read_csv('newcsv3.csv', names = ['Date','House_Price'])
print(df.head())

df.rename(columns={'House_Price':'Prices'}, inplace=True)
print(df.head())
 
