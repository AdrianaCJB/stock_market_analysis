#SOURCE: https://github.com/atreadw1492/yahoo_fin/blob/master/yahoo_fin/stock_info.py
# finviz:  https://www.youtube.com/watch?v=cGL1FJKEfAk
# https://theautomatic.net/yahoo_fin-documentation/



import pandas as pd
from yahoo_fin import stock_info as si
from datetime import datetime, time


tickers_spy    = pd.DataFrame( si.tickers_sp500())
tickers_nasdaq = pd.DataFrame( si.tickers_nasdaq())
tickers_dow    = pd.DataFrame( si.tickers_dow())





def get_data_startdate(ticker, start_date):
     return si.get_data(ticker , start_date = start_date)


def get_cleaned_data_startdate(ticker, start_date):
    df = get_data_startdate(ticker , start_date)
        
    ## GAP up or GAP down.
    df["prev_close"] = df.close.shift(1)
    df['chg%_premarket'] = 100*-1*df[['open','prev_close']].pct_change(axis=1)['prev_close'].round(5)

    ## Cuanto movió en el dia.
    df['chg%_intraday'] =  100*-1*((df['open'] - df['close'])/df['close']).round(5)

    df.reset_index(inplace=True)
    df.rename(columns={"index":"Date"},inplace=True)

    return df



def create_change_percentajes(df):
    
    df["prev_close"] = df.close.shift(1)

    df['chg%_premarket'] = 100*-1*df[['open','prev_close']].pct_change(axis=1)['prev_close'].round(5)

    ## Cuanto movió en el dia.
    df['chg%_intraday'] =  100*-1*((df['open'] - df['close'])/df['close']).round(5)
    
    return df



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
    
    
    
def get_earnings_history(ticker):
    return si.get_earnings_history(ticker)


def prepare_data_for_earnings(ticker, start_date):
    cols_print = ['Date','chg%_premarket', 'chg%_intraday']


    df = get_cleaned_data_startdate(ticker , start_date)[cols_print]
        
    ## conocer el comportamiento el dia antes, el dia del earning y dia despues.
    df["yesterday_chg%_intraday"] = df['chg%_intraday'].shift(1)
    df["tomorrow_chg%_intraday"] = df['chg%_intraday'].shift(-1)
    
    df.rename(columns={"chg%_intraday":"today_chg%_intraday"},inplace=True)
    
    order = ["Date","yesterday_chg%_intraday","chg%_premarket","today_chg%_intraday", "tomorrow_chg%_intraday"]
    

    return df[order]


def get_processed_earnings_history(ticker):

    start_market = time(9, 30, 0)
    end_market = time(16, 0, 0)
    

    
    dict_EPS = get_earnings_history(ticker)
    df = pd.DataFrame.from_dict(dict_EPS)

    df["Time_EPS"] = df['startdatetime']\
                    .apply(lambda val: datetime.strptime(val, '%Y-%m-%dT%H:%M:%S.%f%z')\
                    .time())

    df["Date_EPS"] = df['startdatetime']\
                    .apply(lambda val: datetime.strptime(val, '%Y-%m-%dT%H:%M:%S.%f%z')\
                    .date())

    df["Date_EPS"] = df["Date_EPS"].astype('datetime64[ns]')
    
    
    df.loc[df['Time_EPS'] < start_market, 'Time Report'] = 'BMO'  ## before markets open
    df.loc[df['Time_EPS'] > end_market , 'Time Report'] = 'AMC'  ## after markets close
    #df.loc[(df['Time_EPS'] > start_market & df['Time_EPS'] < end_market), 'Time Report'] = 'MO'  ## markets open
    
    
    return df



    
def convert_currency_column(amount):
    return "${:,.0f}".format(amount)


def convert_quarters_to_currency_format(df):
    
    for i in range(1,5):
        df.iloc[:, i] = df.iloc[:, i].apply(lambda x: 0 if x is None else x)
        df.iloc[:, i] = df.iloc[:, i].apply(convert_currency_column)
        
    return df