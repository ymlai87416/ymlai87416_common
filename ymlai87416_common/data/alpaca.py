# https://algotrading101.com/learn/alpaca-trading-api-guide/
# this program is to download 1 min data for apple.
# 2021-3-23 Update API to get_bars
import alpaca_trade_api as tradeapi
import yaml
import pandas as pd
from datetime import datetime, timedelta
if __name__ == '__main__':
    import utilities
else:
    from . import utilities
import os

# Alpaca
# Said it is for stock and crypto trading
# Stock is ok, and provide 1 min data
# Crypto not quite, only show popular coin, better not use
#

def __read_secret():
    # read from secret
    secret_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "..", "secret.yaml")
    with open(secret_path, "r") as stream:
        try:
            data = yaml.safe_load(stream)
            alpaca_paper_endpoint = data['alpaca_paper_endpoint']
            alpaca_api_key = data['alpaca_api_key']
            alpaca_api_secret = data['alpaca_api_secret']

            return (alpaca_paper_endpoint, alpaca_api_key, alpaca_api_secret)

        except yaml.YAMLError as exc:
            print(exc)
            exit()


def __read_secret2(data):
    '''
    Read secret from data

    Parameters
    ----------
    data: dict
        a dictinary of secret

    Returns
    -------
    secret: tuple
        return following in orders: alpaca_paper_endpoint, alpaca_api_key, alpaca_api_secret
    '''

    alpaca_paper_endpoint = data['alpaca_paper_endpoint']
    alpaca_api_key = data['alpaca_api_key']
    alpaca_api_secret = data['alpaca_api_secret']

    return (alpaca_paper_endpoint, alpaca_api_key, alpaca_api_secret)

def get_olhc_1min(symbol: str, date_start: datetime, date_end: datetime, config):
    '''
    Read 1 min data from alpaca api

    Parameters
    ----------
    symbol: string
        stock symbol
    start date: datetime
        start date - inclusive
    end date: datetime
        end date - inclusive

    Returns
    -------
    df_bar: pandas.DataFrame
        olhc in 1 minutes
    '''
    
    (alpaca_paper_endpoint, alpaca_api_key, alpaca_api_secret) = __read_secret2(config)

    api = tradeapi.REST(alpaca_api_key, alpaca_api_secret, alpaca_paper_endpoint, api_version='v2')
    # 1 day = 390 minutes
    # 1 month = 12090
    # alpaca accept 1000 bar
    #df_bar = pd.DataFrame(columns = ['Close','High', 'Low', 'Open', 'Time', 'Volume'])
    df_bar = utilities.get_olhc_df()
    date_range = pd.date_range(date_start, date_end,freq='d')

    for d in date_range:
        starttime = '%d-%02d-%02dT09:30:00-05:00' % (d.year, d.month, d.day)
        endtime = '%d-%02d-%02dT16:00:00-05:00' % (d.year, d.month, d.day)
        #print(d, starttime, endtime)
        
        barset = api.get_bars(symbol, '1Min', limit=390, start=starttime, end=endtime)
        #print("DD", barset)
        #for bark in barset.keys():
        for bar in barset:
            df_bar = df_bar.append({'Close': bar.c, 'High': bar.h, 'Low': bar.l, 'Open': bar.o, 'Time': bar.t, 'Volume': bar.v,}, ignore_index=True)

    df_bar.set_index('Time', inplace=True)

    return df_bar


def get_olhc(symbol: str, date_start: datetime, date_end: datetime, config):
    '''
    Make use of alpaca api to get 1 min of data
    API explanation at: 

    Args:
        symbol: stock symbol
        start date: inclusive
        end date: inclusive

    Returns: olhc in 1 minutes
    '''

    (alpaca_paper_endpoint, alpaca_api_key, alpaca_api_secret) = __read_secret2(config)

    api = tradeapi.REST(alpaca_api_key, alpaca_api_secret, alpaca_paper_endpoint, api_version='v2')
    df_bar = df_bar = utilities.get_olhc_df()

    starttime = '%d-%02d-%02dT09:30:00-05:00' % (date_start.year, date_start.month, date_start.day)
    endtime = '%d-%02d-%02dT16:00:00-05:00' % (date_end.year, date_end.month, date_end.day)
    #print(d, starttime, endtime)
    
    barset = api.get_bars(symbol, '1Day', start=starttime, end=endtime)

    #for bark in barset.keys():
    for bar in barset:
        df_bar = df_bar.append({'Close': bar.c, 'High': bar.h, 'Low': bar.l, 'Open': bar.o, 'Time': bar.t, 'Volume': bar.v,}, ignore_index=True)

    df_bar.set_index('Time', inplace=True)

    return df_bar


if __name__ == '__main__':

    start_date = datetime(2022, 1, 1)
    end_date = datetime(2022, 1, 10)
    print(get_olhc_1min('NVDA', end_date, end_date))
    print(get_olhc('NVDA', start_date, end_date))