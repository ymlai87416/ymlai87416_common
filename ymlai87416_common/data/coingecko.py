from math import e
from this import d
from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json
from datetime import datetime, timedelta
from warnings import warn
import pandas as pd

if __name__ == '__main__':
    import utilities
else:
    from . import utilities
import os

# Coingecko
# No API key is required for coin gecko
# Seems the best data source I can have, but the API is a little bit limited

# TODO: Should be obsolete and provide from outside
def __symbol_to_id(symbol: str):
    gecko_id = {
        'eth': 'ethereum',
        'bnb': 'binancecoin',
        'ceek': 'ceek', 
        'bit': 'bitdao',
        'usdt': 'tether',
        'busd': 'binance-usd',
        'kasta': 'kasta',
        'thc': 'thetan-coin',
        'pi': '???',
        'sol': 'solana',
        'aca': 'acala',
        'matic': 'matic-network',
        'bdot': 'binance-wrapped-dot',
        'weth-polygon': 'ethereum',
    }

    return gecko_id.get(symbol.lower())


def get_all_symbol():
    url = 'https://api.coingecko.com/api/v3/coins/list'
    #print(symbol, url)

    headers = {
        'Accepts': 'application/json',
    }

    params = {
        'include_platform': "true",
    }
    session = Session()
    session.headers.update(headers)

    try:
        response = session.get(url, params=params)
        data = json.loads(response.text)
        print(response.text)
        f = open("gecko.txt", "r", encoding='UTF-8')
        f.write(json.dumps(data))
        f.close()
    except:
        pass

def read_olhc():
    f = open('gecko_olhc.txt',)
    data = json.load(f)

    for i in data:
        print(i)


def get_olhc(symbol: str, days: int):
    '''
    from: https://www.coingecko.com/zh/api/documentation?__cf_chl_jschl_tk__=de.CxkBvFf7M.PljTfKXApzLNgZA_hcVoNIp9TVAQWw-1641851212-0-gaNycGzNChE
    Candle's body:

    1 - 2 days: 30 minutes
    3 - 30 days: 4 hours
    31 and before: 4 days
    1/7/14/30/90/180/365/max

    Parameters
    ----------
    symbol: string
        crypto symbol
    days: int
        Range of days, day back from today, beware can only be 1/7/14/30/90/180/365/max
    
    Returns 
    -------
    df_bar: pandas.DataFrame
        olhc in whatever time range specified by coin gecko
    '''

    url = 'https://api.coingecko.com/api/v3/coins/%s/ohlc' % __symbol_to_id(symbol)

    headers = {
        'Accepts': 'application/json',
    }

    value_days =[1,7,14,30,90,180,365]

    if days > 365:
            days = "max"
    else:
        for v in value_days:
            if days <= v:
                days = v
                break
    

    params = {
        'vs_currency': "usd",
        'days': days, 
    }
    session = Session()
    session.headers.update(headers)

    try:
        df = utilities.get_olhc_df()
        
        response = session.get(url, params=params)
        data = json.loads(response.text)

        for rec in data: 
            rec_time = datetime.utcfromtimestamp(rec[0]/1000)

            df = df.append({
                'Close': rec[4] ,'High': rec[2], 'Low': rec[3], 'Open': rec[1], 'Time': rec_time, 'Volume': 0 
            }, ignore_index=True)

        df.set_index('Time', inplace=True)
        df = utilities.resample_df(df)
        return df
    except Exception as e:
        print(e)


def get_price(symbol: str, date_from: datetime, date_to: datetime):
    '''
    Get price of a crypto currency within a time range

    Parameters
    ----------
    symbol: string
        crypto symbol
    date_from: datetime
        start date
    date_to: datetime
        end date
    
    Returns 
    -------
    df_bar: pandas.DataFrame
        price, market_cap and total_volume of each day
    '''

    start_unix_time = int(date_from.timestamp())
    end_unix_time = int(date_to.timestamp())

    url = 'https://api.coingecko.com/api/v3/coins/%s/market_chart/range?vs_currency=usd&from=%d&to=%d' % (symbol, start_unix_time, end_unix_time)

    headers = {
        'Accepts': 'application/json',
    }
    session = Session()
    session.headers.update(headers)

    try:
        df = utilities.get_olhc_df()

        response = session.get(url)
        data = json.loads(response.text)
        price_list = data['prices']
        #market_list = data['market_caps']
        volume_list = data['total_volumes']

        df_price = pd.DataFrame(price_list, columns = ['Time', 'Price'])
        df_volume = pd.DataFrame(volume_list, columns = ['Time', 'Volume'])
        df_full = pd.merge(df_price, df_volume, on='Time')
        df_full.set_index('Time', inplace=True)
        df_full.sort_index()
        prev_close = -1

        for index, row in df_full.iterrows():
            #print("DD", index, row)
            rec_time = datetime.utcfromtimestamp(index/1000)
            close = row['Price']
            volume = row['Volume']
            if prev_close == -1:
                prev_close = close

            high = max(prev_close, close)
            low = min(prev_close, close)

            #print("DD", rec_time, close, volume, prev_close, high, low)

            df = df.append({
                'Close': close ,'High': high, 'Low': low, 'Open': prev_close, 'Time': rec_time, 'Volume': volume 
            }, ignore_index=True)

            prev_close = close

        #print(df)

        df.set_index('Time', inplace=True)
        df = utilities.resample_df(df)
        return df
    except Exception as e:
        print("exception", e)


if __name__ == '__main__':

    query_crypto = ['bitcoin', 'ethereum', 'solana', 'avalanche-2']
    start_date = datetime.today() + timedelta(days=-14)
    end_date = datetime.today()

    for symbol in query_crypto:
        #df_bar = get_olhc(symbol, 14)
        df_bar = get_price(symbol, start_date, end_date)
        print(df_bar)
        # download and save it to other place
        #df_bar.to_csv('%s_%s.csv' % (symbol, datetime.today().strftime("%Y-%m-%d")))


        break
