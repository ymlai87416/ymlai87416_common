# This is the stock module
# Extract coin info from either cryptowatch or pancakeswap
import pandas as pd
from . import alphavantage
from . import alpaca
from datetime import datetime

def __get_olhc_us(symbol: str, date_from: datetime, date_to: datetime, config):
    return alpaca.get_olhc(symbol, date_from, date_to, config)

def __get_olhc_hk(symbol: str, date_from: datetime, date_to: datetime, config):
    pass

def get_olhc(symbol: str, date_from: datetime, date_to: datetime, region: str, config):
    '''
    Get OLHC data

    Parameters
    ----------
    symbol: string
        stock symbol
    date_from: datetime
        start date - inclusive
    date_to: datetime
        end date - inclusive
    region: string
        region of the stock
    config 
        configuration
    '''
    if region.lower() == "us":
        return __get_olhc_us(symbol, date_from, date_to, config)
    elif region.lower() == "hk":
        return __get_olhc_hk(symbol, date_from, date_to, config)
    else: 
        raise ValueError("region not yet supported.")

def __get_fundamentals_us(symbol, config):
    return alphavantage.get_fundamental(symbol, config)

def __get_fundamentals_hk(symbol, config):
    pass

def get_fundamentals(symbol, region, config):
    if region.lower() == "hk":
        return __get_fundamentals_hk(symbol, config)
    elif region.lower() == "us":
        return __get_fundamentals_us(symbol, config)
    else: 
        raise ValueError("region not yet supported.")

def get_option_chart(symbol, region, config):
    pass
