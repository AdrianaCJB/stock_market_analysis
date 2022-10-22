#SOURCE: https://github.com/atreadw1492/yahoo_fin/blob/master/yahoo_fin/stock_info.py
# finviz:  https://www.youtube.com/watch?v=cGL1FJKEfAk
# https://theautomatic.net/yahoo_fin-documentation/



import pandas as pd
from yahoo_fin import stock_info as si

tickers_spy    = pd.DataFrame( si.tickers_sp500())
tickers_nasdaq = pd.DataFrame( si.tickers_nasdaq())
tickers_dow    = pd.DataFrame( si.tickers_dow())



def get_data_startdate(ticker, start_date):
     return si.get_data(ticker , start_date = start_date)


## Get stats valuation and financials


def get_stats(ticker):
    return si.get_stats(ticker)

def get_stats_valuation(ticker):
    return si.get_stats_valuation(ticker)


def get_financials(ticker, yearly_flag = True, quarterly_flag = True):
    return si.get_financials(ticker, yearly_flag, quarterly_flag)


def get_income_statement(ticker):
    return si.get_income_statement(ticker)


def get_day_most_active():
    return si.get_day_most_active()


def get_day_gainers():
    return si.get_day_gainers()


def get_day_losers():
    return si.get_day_losers()



## Format dataframes and columns

def convert_dataframe_reset_index(df):
    df.reset_index(inplace=True)
    return df

    
def rename_columns_dataframe(df):
    from datetime import datetime
    import pandas as pd

    colum_list = df.columns.tolist()
    new_list = []

    for col in colum_list:
        if (type(col) == pd._libs.tslibs.timestamps.Timestamp):
            dt_object = col.date()
            date_time_obj = pd.to_datetime(dt_object)
            col = str(date_time_obj.year) + "Q" + str(date_time_obj.quarter)

        new_list.append(col)

    df.columns = new_list
    return df
    
    
    
def convert_currency_column(amount):
    return "${:,.0f}".format(amount)


def convert_quarters_to_currency_format(df):
    
    for i in range(1,5):
        df.iloc[:, i] = df.iloc[:, i].apply(lambda x: 0 if x is None else x)
        df.iloc[:, i] = df.iloc[:, i].apply(convert_currency_column)
        
    return df