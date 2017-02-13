#!/usr/bin/env python3

from NseMarketData import NseMarketData
import os, argparse
from flask import Flask, make_response, send_file
from flask_restful import Api, Resource, reqparse, abort
import pandas as pd
from pandas_datareader import data, wb, Options
import matplotlib.pyplot as plt
import datetime
from matplotlib.finance import quotes_historical_yahoo_ohlc, candlestick_ohlc
from matplotlib.dates import date2num, DateFormatter
from datetime import datetime
import json

parser=argparse.ArgumentParser()
#parser.add_argument('-w','--work_dir',required=True, help='Work directory')
#parser.add_argument('-p','--host', default='127.0.0.1', help='REST api host ip')
args=parser.parse_args()

#work_dir   = args.work_dir
#host       = args.host

app=Flask(__name__)
api=Api(app)



if __name__=='__main__':
  data=NseMarketData(url='http://www.moneycontrol.com/stocks/marketstats/indexcomp.php?optex=NSE&opttopic=indexcomp&index=9')
  json_data=data.get_market_data_json()
  print(json.dumps(json_data, indent=4)) 
