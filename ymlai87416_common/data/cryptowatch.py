
import yaml
from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json
from datetime import datetime, timedelta
import pandas as pd
if __name__ == '__main__':
    import utilities
else:
    from . import utilities
import os

# Crytowatch
# Also a data provider, but seems a lot to catch up

#crypto watch have a much difficult api, and I have to specify the market, which just I don't know

def __read_secret(data):
    cryptowatch_public_key = data['cryptowatch_public_key']
    return cryptowatch_public_key

def get_olhc(crypto_symbol, start_date, end_date, period, config):
    '''
    Get olhc data from cryptowatch

    Parameters
    ----------
    crypto_symbol: string
        crypto symbol
    start_date: datetime
        start date - inclusive
    end_date: datetime
        end date - inclusive
    period: int
        period in seconds, e.g. 1D = 86400 seconds
    config: dict
        configuration
    '''

    # read from secret
    cryptowatch_public_key = __read_secret(config)

    df_bar = utilities.get_olhc_df()

    # TODO: may need to check check binance-us, but whatever
    url = 'https://api.cryptowat.ch/markets/binance-us/%susd/ohlc' %  crypto_symbol

    headers = {
        'Accepts': 'application/json',
        'X-CW-API-Key': cryptowatch_public_key,
    }

    params = {
        'after': int(datetime.timestamp(start_date)),
        'before': int(datetime.timestamp(end_date)),
        'periods' : period,
    }
    session = Session()
    session.headers.update(headers)

    try:
        response = session.get(url, params=params)
        data = json.loads(response.text)
        
        #print(json.dumps(data))
        # download and save it to other place
        for rec in data["result"]["86400"]:
            date_rec = datetime.utcfromtimestamp(rec[0])
            df_bar = df_bar.append({'Close': rec[4], 'High': rec[2], 'Low': rec[3], 'Open': rec[1], 'Time': date_rec, 'Volume': rec[6],}, ignore_index=True)

        df_bar.set_index('Time', inplace=True)

        return df_bar

    except (ConnectionError, Timeout, TooManyRedirects) as e:
        print(e)

if __name__ == '__main__':
    secret_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "..", "..","..", "secret.yaml")
    stream = open(secret_path, "r")
    data = yaml.safe_load(stream)

    query_crypto = ['MATIC', 'ETH', 'SOL', 'AVAX']
    start_date = datetime.today() + timedelta(days=-14)
    end_date = datetime.today()

    for symbol in query_crypto:
        df_bar = get_olhc(symbol, start_date, end_date, 86400, data)

        # download and save it to other place
        df_bar.to_csv('%s_%s.csv' % (symbol, datetime.today().strftime("%Y-%m-%d")))