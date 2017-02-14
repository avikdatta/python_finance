#!/usr/bin/env python3

import matplotlib
# Force matplotlib to not use any Xwindows backend.
matplotlib.use('Agg')

import os
import pandas as pd
from pandas_datareader import data, wb, Options
import matplotlib.pyplot as plt
import datetime
from matplotlib.finance import quotes_historical_yahoo_ohlc, candlestick_ohlc
from matplotlib.dates import date2num, DateFormatter
from datetime import datetime
import json
from utils import get_temp_dir, clean_temp_dir


class NseStockData:

  def __init__(self, stock, date, work_dir, server='yahoo', date_window=None, small_window=15, large_window=50, fig_height=8, fig_width=12, fig_font=10):
    self.stock=stock
    self.date=date
    self.work_dir=work_dir
    self.date_window=date_window
    self.server=server
    self.small_window=small_window
    self.large_window=large_window
    self.fig_height=fig_height
    self.fig_width=fig_width
    self.fig_font=fig_font


  def _get_moving_average(self):
    '''
    Calculate moving average of a given stock
    Input: Stock symbol and start date
    Output: Dataframe containing MA15, MA50 and EMA15 values and data array
    '''
    # fetch data from yahoo server
    nse_data=data.DataReader(self.stock, self.server, self.date)
    
    
    # set values for moving average calculation    
    d_small=nse_data['Adj Close'].rolling(window=self.small_window)
    d_large=nse_data['Adj Close'].rolling(window=self.large_window)
    
    # add small_MA and large_MA values to the dataframe    
    nse_data=pd.concat([nse_data, pd.Series(d_small.mean(), name='MA{}'.format(self.small_window)),
              pd.Series(d_large.mean(),name='MA{}'.format(self.large_window))], axis=1).dropna()
    nse_data.reset_index(inplace=True)

    nse_data=self._calculate_ema_value(self.small_window, nse_data, 'EMA{}'.format(self.small_window), nse_data.at[0, 'MA{}'.format(self.small_window)])
    nse_data=self._calculate_ema_value(self.large_window, nse_data, 'EMA{}'.format(self.large_window), nse_data.at[0, 'MA{}'.format(self.large_window)])

    
    # set index for data frame
    nse_data=nse_data.set_index('Date')        
    nse_data['Dates']=date2num(nse_data.index.to_pydatetime())
    
    # reset date window
    if self.date_window:
        nse_data=nse_data[-self.date_window:-1]
    
    # generate data_array for matplotlib candlelstick plot
    data_array=[tuple(x) 
            for x in nse_data[['Dates','Open','High','Low','Adj Close']].
            to_records(index=False)]
    
    return nse_data, data_array

  def _calculate_ema_value(self, window, nse_data, lable, first_val):
    '''
    A function for calculating exponential MA values for a given window
    '''

    # add empty EMA value
    nse_data[lable]=''
    
    # add first EMA value
    nse_data=nse_data.set_value(0,lable,first_val)

    # calculate EMA values
    sf=2/(window+1)
    for index, val in enumerate(nse_data[lable]):
      if val == '':
        ema_val=(nse_data.at[index, 'Adj Close'] - nse_data.at[index-1, lable]) * sf + nse_data.at[index,'Adj Close']  
        nse_data=nse_data.set_value(index, lable, ema_val)
    return nse_data

  def _plot_ma_data(self, nse_data, nse_data_arr):
    '''
    A function for plotting MA data
    '''

    try:
      temp_dir=get_temp_dir(work_dir=self.work_dir)
      os.chdir(temp_dir)
      date_format=DateFormatter('%b %y')
      filename='{}_{}_{}_{}.png'.format(self.stock, self.date, self.small_window, self.large_window)
      filename=os.path.join(temp_dir,filename)
      title='{}_{}_{}_{}'.format(self.stock, self.date, self.small_window, self.large_window)

      # plot data

      plt.figure(figsize=(self.fig_width, self.fig_height))
      fig,ax=plt.subplots()
      ax.xaxis_date()
      ax.xaxis.set_major_formatter(date_format)
      mlp=candlestick_ohlc(ax, nse_data_arr, width=0.7, colorup='g', colordown='r' )
      nse_data['MA{}'.format(self.small_window)].plot(style='-', alpha=0.5, color='orange', label='MA{}'.format(self.small_window))
      nse_data['MA{}'.format(self.large_window)].plot(style='-', alpha=0.5, color='blue', label='MA{}'.format(self.large_window))
      nse_data['EMA{}'.format(self.small_window)].plot(style='-', alpha=0.5, color='purple', label='EMA{}'.format(self.small_window))
      nse_data['EMA{}'.format(self.large_window)].plot(style='-', alpha=0.5, color='lime', label='EMA{}'.format(self.large_window))
      handles, labels = ax.get_legend_handles_labels()
      ax.legend(handles, labels, loc='best', fontsize=8)
      plt.title(title)
      plt.savefig(filename,bbox_inches='tight')
      plt.close("all")

    except Exception as e:
      print('Error {}'.format(e))
      clean_temp_dir(temp_dir=temp_dir)
    else:
      return filename, temp_dir

if __name__=='__main__':
  t1=NseStockData(stock='ADANIPORTS.NS', date='2016-01-01', date_window=20, work_dir='/root/app')
  t1_data, t1_array=t1._get_moving_average()
  filename, temp_dir=t1._plot_ma_data(t1_data, t1_array)
  print(filename)
