# This is the crypto module
# Extract coin info from either cryptowatch or pancakeswap

from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
from datetime import datetime, timedelta
import pandas as pd
from . import coingecko
from . import cryptowatch

# TODO: Should be obsolete and provide from outside
def translate_coingecko_id(symbol):
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


def get_olhc(symbol: str, date_from: datetime, date_to: datetime, config):
    '''
    Multiple provider: cryptowatch, pancake swap api, and also coingecko.

    Parameters
    ----------
    symbol: string
        crypto symbol
    date_from: datetime
        start date - inclusive
    date_to: datetime
        end date - inclusive
    config: dict
        configuration dictionary

    Returns
    -------
    df: pandas.DataFrame
        olhc in at least 1 day
    '''
    # if both date_from and date_to are within 30 day of today, use coingecko, else use cryptowatch
    date_30_before = datetime.today().date() + timedelta(days=-30)
    if date_from >= date_30_before: # coin gecko return 4 hours for below 30 days
        symbol2 = translate_coingecko_id(symbol)
        df =  coingecko.get_olhc(symbol2, abs((date_from - datetime.today().date()).days))
        if not df is None:
            df = df.loc[date_from:date_to]
        return df
    else:
        try:
            return cryptowatch.get_olhc(symbol, date_from, date_to, config)
        except:
            return None