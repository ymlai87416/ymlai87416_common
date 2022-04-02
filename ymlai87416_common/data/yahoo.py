from datetime import datetime, timedelta
import yfinance as yf
from pandas_datareader import data as pdr
yf.pdr_override()

def get_olhc_us(ticker: str, date_from: datetime, date_to: datetime):
    '''
    Get OHLC data from Yahoo Finance for US stocks.
    
    Parameters
    ----------
    ticker : str
        Ticker of the stock. e.g. MSFT
    date_from : datetime
        Start date of the data. inclusive
    date_to : datetime
        End date of the data. inclusive

    Returns
    -------
    result: pandas.DataFrame
        OHLC data of the stock.
    '''
    _date_from = date_from.strftime('%Y-%m-%d')
    _date_to = date_to.strftime('%Y-%m-%d')
    data = pdr.get_data_yahoo(ticker, start=_date_from, end=_date_to)
    return data


def get_olhc_hk(ticker: str, date_from: datetime, date_to: datetime):
    '''
    Get OHLC data from Yahoo Finance for HK stocks.
    
    Parameters
    ----------
    ticker : str
        Ticker of the stock. e.g. MSFT
    date_from : datetime
        Start date of the data.
    date_to : datetime
        End date of the data.

    Returns
    -------
    result: pandas.DataFrame
        OHLC data of the stock.
    '''
    _date_from = date_from.strftime('%Y-%m-%d')
    _date_to = date_to.strftime('%Y-%m-%d')
    data = pdr.get_data_yahoo(ticker, start=_date_from, end=_date_to) 
    return data


def get_info_us(ticker: str):
    '''
    Get info from Yahoo Finance for US stocks.

    Parameters
    ----------
    ticker : str
        Ticker of the stock. e.g. MSFT
    
    Returns
    -------
    result: dict
        Basic info of the stock.
    '''
    _ticker = yf.Ticker(ticker)
    return _ticker.info

def get_info_hk(ticker: str):
    '''
    Get info from Yahoo Finance for HK stocks.

    Parameters
    ----------
    ticker : str
        Ticker of the stock. e.g. 0005.HK
    
    Returns
    -------
    result: dict
        Basic info of the stock.
    '''
    _ticker = yf.Ticker(ticker)
    return _ticker.info


if __name__ == '__main__':
    
    #msft = yf.Ticker("0005.HK")
    data = pdr.get_data_yahoo("SCO", start='2022-1-1', end='2022-3-30')
    # get stock info
    print(data)