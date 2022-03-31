import pandas as pd
from collections import OrderedDict

def get_fundamental_df():
    df_info = pd.DataFrame(columns = ['Symbol',
        'op_income_Y1', 'op_income_Y2', 'op_income_Y3', 'op_income_Y4', 'op_income_Y5',
        'net_income_Y1', 'net_income_Y2', 'net_income_Y3', 'net_income_Y4', 'net_income_Y5',
        'roe_Y1', 'roe_Y2', 'roe_Y3', 'roe_Y4', 'roe_Y5',
        'gross_margin_Y1', 'gross_margin_Y2', 'gross_margin_Y3', 'gross_margin_Y4', 'gross_margin_Y5',
        'cash_div_Y1', 'cash_div_Y2', 'cash_div_Y3', 'cash_div_Y4', 'cash_div_Y5',
        'beta'
        ])

    return df_info

def get_olhc_df():
    df_bar = pd.DataFrame(columns = ['Close','High', 'Low', 'Open', 'Time', 'Volume'])
    return df_bar

def get_option_chain_df():
    pass

def resample_df(df):
    df = df.resample('D').agg(
    OrderedDict([
        ('Open', 'first'),
        ('High', 'max'),
        ('Low', 'min'),
        ('Close', 'last'),
        ('Volume', 'sum'),
    ])
    )
    return df
