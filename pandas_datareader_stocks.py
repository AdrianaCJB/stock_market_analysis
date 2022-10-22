#SOURCE: https://github.com/atreadw1492/yahoo_fin/blob/master/yahoo_fin/stock_info.py
# finviz:  https://www.youtube.com/watch?v=cGL1FJKEfAk
# https://theautomatic.net/yahoo_fin-documentation/



import pandas as pd
import pandas_datareader.data as pdr



def get_ticker(ticker,start_date, end_date):

    return pdr.DataReader(ticker, 'yahoo', start_date, end_date)