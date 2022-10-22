#SOURCE: https://github.com/atreadw1492/yahoo_fin/blob/master/yahoo_fin/stock_info.py
# finviz:  https://www.youtube.com/watch?v=cGL1FJKEfAk
# https://theautomatic.net/yahoo_fin-documentation/



import pandas as pd
import pandas_datareader.data as pdr



def get_ticker(ticker,start_date, end_date):

    return pdr.DataReader(ticker, 'yahoo', start_date, end_date)



def get_cleaned_data_ticker(ticker,start_date, end_date):

    ## GAP up or GAP down.
    df = get_ticker(ticker,start_date, end_date)
    df["prev_close"] = df.Close.shift(1)
    df['chg%_premarket'] = 100*-1*df[['Open','prev_close']].pct_change(axis=1)['prev_close'].round(5)
    df.reset_index(inplace=True)
    return df


