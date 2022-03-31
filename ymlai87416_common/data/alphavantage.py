import yaml
import pandas as pd
from datetime import datetime, timedelta
import requests
import os

# Alpha vantage
# Free API key: (5 API requests per minute; 500 API requests per day)
# Currently I only test out of stock function, but really the limit is too low to proceed.
# Even getting fundamental data need throttling, but only this company provide?
# IB fundamental need Wall Street Events Horizon Calendar (USD$5 each month as of 27th Mar)

if __name__ == '__main__':
    import utilities
else:
    from . import utilities

def __get_alpha_vantage_key():
    # read from secret
    secret_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "..", "secret.yaml")
    with open(secret_path, "r") as stream:
        try:
            data = yaml.safe_load(stream)
            return __get_alpha_vantage_key2(data)
        except yaml.YAMLError as exc:
            print(exc)
            exit()

def __get_alpha_vantage_key2(data):
    '''
    Read secret from a dictionary

    Parameters
    ----------
    data: dict
        Dictionary containing the secret
    
    Returns
    -------
    alphavantage_key: str
        Alpha Vantage API key

    '''
    alphavantage_key = data['alphavantage_key']
    return alphavantage_key

def get_fundamental(symbol, config):
    '''
    Get key fundamental data from Alpha Vantage

        Most important factor beside PE ratio, and I also have to know if it have updated?
        operating income: (from income statement -> operatingIncome)
        net income (from income statement -> netIncome)
        ROE > 15% ROE = net income / share holder equity (balance sheet: totalShareholderEquity)
        Gross margin increase 5 years (incomestatement: totalRevenue - costOfRevenue)
        Cash dividend increase 5 years (cashflow: dividendPayoutCommonStock / balancesheet: )
        Beta: ???

    TODO: Confirm all fundamental data are correct

    Parameters
    ----------
    symbol: str
        Stock symbol
    config: dict
        Dictionary containing the configuration

    Returns
    -------
    data: dict
        Return a list of fundamental data

    '''
    df = utilities.get_fundamental_df()
    incomeStatement = get_income_statement(symbol, config)
    balanaceSheet = get_balance_sheet(symbol, config)
    cashFlow = get_cashflow(symbol, config)
    overview = get_overview(symbol, config)

    #cofirm there is at least 5 annual report using 
    annual_report_len = len(incomeStatement["annualReports"])

    op_income = [0, 0, 0, 0, 0]
    net_income = [0, 0, 0, 0, 0]
    roe = [0, 0, 0, 0, 0]
    gross_margin = [0, 0, 0, 0, 0]
    cash_div = [0, 0, 0, 0, 0]

    beta = float(overview["Beta"])

    for i in range(0, min(annual_report_len, 5)):
        t_op_income = float(incomeStatement["annualReports"][i]["operatingIncome"])
        t_net_income = float(incomeStatement["annualReports"][i]["netIncome"])
        t_total_revenue = float(incomeStatement["annualReports"][i]["totalRevenue"])
        t_cogs = float(incomeStatement["annualReports"][i]["costofGoodsAndServicesSold"])
        t_share_outstanding =  int(balanaceSheet["annualReports"][i]["commonStockSharesOutstanding"])
        t_dividendPayoutCommon = float(cashFlow["annualReports"][i]["dividendPayoutCommonStock"])
        op_income[i] = t_op_income
        net_income[i] = t_net_income
        roe[i] = t_net_income / t_share_outstanding
        gross_margin[i] = (t_total_revenue - t_cogs) / t_total_revenue
        cash_div[i] =  t_dividendPayoutCommon / t_share_outstanding

    df = df.append({
        'Symbol': symbol,
        'op_income_Y1': op_income[0], 'op_income_Y2': op_income[1], 'op_income_Y3': op_income[2], 'op_income_Y4': op_income[3], 'op_income_Y5': op_income[4],
        'net_income_Y1': net_income[0], 'net_income_Y2': net_income[1], 'net_income_Y3': net_income[2], 'net_income_Y4': net_income[3], 'net_income_Y5': net_income[4],
        'roe_Y1': roe[0], 'roe_Y2': roe[1], 'roe_Y3': roe[2], 'roe_Y4': roe[3], 'roe_Y5': roe[4],
        'gross_margin_Y1': gross_margin[0], 'gross_margin_Y2': gross_margin[1], 'gross_margin_Y3': gross_margin[2], 'gross_margin_Y4': gross_margin[3], 'gross_margin_Y5': gross_margin[4],
        'cash_div_Y1': cash_div[0], 'cash_div_Y2': cash_div[1], 'cash_div_Y3': cash_div[2], 'cash_div_Y4': cash_div[3], 'cash_div_Y5': cash_div[4],
        'beta': beta
    }, ignore_index=True)


    return df


def get_income_statement(symbol, config):
    alphavantage_key = __get_alpha_vantage_key2(config) 

    param = {
        "function": "INCOME_STATEMENT", 
        "symbol": symbol,
        "apikey": alphavantage_key, 
    }
    url = "https://www.alphavantage.co/query"
    res = requests.get(url, param)
    #html = f.content()
    #print(res.json())

    return res.json()


def get_balance_sheet(symbol, config):

    alphavantage_key = __get_alpha_vantage_key2(config) 

    param = {
        "function": "BALANCE_SHEET", 
        "symbol": symbol,
        "apikey": alphavantage_key, 
    }
    url = "https://www.alphavantage.co/query"
    res = requests.get(url, param)
    #html = f.content()
    #print(res.json())

    return res.json()


def get_cashflow(symbol, config):

    alphavantage_key = __get_alpha_vantage_key(config) 

    param = {
        "function": "CASH_FLOW", 
        "symbol": symbol,
        "apikey": alphavantage_key, 
    }
    url = "https://www.alphavantage.co/query"
    res = requests.get(url, param)
    #html = f.content()
    #print(res.json())

    return res.json()

def get_earnings(symbol, config):

    alphavantage_key = __get_alpha_vantage_key(config) 

    param = {
        "function": "EARNINGS", 
        "symbol": symbol,
        "apikey": alphavantage_key, 
    }
    url = "https://www.alphavantage.co/query"
    res = requests.get(url, param)
    #html = f.content()
    print(res.json())

    return res.json()

def get_overview(symbol, config):

    alphavantage_key = __get_alpha_vantage_key(config) 

    param = {
        "function": "OVERVIEW", 
        "symbol": symbol,
        "apikey": alphavantage_key, 
    }
    url = "https://www.alphavantage.co/query"
    res = requests.get(url, param)
    #html = f.content()
    #print(res.json())

    return res.json()

def get_earning_calendar():
    # TODO: get earning calendar from alpha vantage
    pass

if __name__ == '__main__':

    print(get_fundamental('AI'))