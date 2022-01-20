from polygon_api.polygon_rest import RESTClient
import pandas as pd
import datetime
from datetime import date, timedelta
import json
from django.http import JsonResponse


def ploygon_stocks_data():
    """ Polygon REST API Implementation """

    key = "_t__ozhe3p5ACaYlHpPk2y4oEj7KkElP"
    with RESTClient(key) as client:
        l = ['SPY', 'QQQ', 'DIA']
        df = pd.DataFrame(columns=['Symbol', 'Close', 'Open', 'High', 'Low'])
        for i in l:
            resp = client.stocks_equities_previous_close(i)
            for result in resp.results:
                close = result['c']
                open = result['o']
                high = result['h']
                low = result['l']
            row = {'Symbol': i, 'Close': close, 'Open': open, 'High': high, 'Low': low}
            df = df.append(row, ignore_index=True)
        df = df.set_index('Symbol')

        spy = df.loc['SPY', 'Close']
        qqq = df.loc['QQQ', 'Close']
        dia = df.loc['DIA', 'Close']
        volatility_spy = round(df.loc['SPY', 'High'] - df.loc['SPY', 'Low'], 2)
        volatility_qqq = round(df.loc['QQQ', 'High'] - df.loc['QQQ', 'Low'], 2)


        return volatility_qqq, volatility_spy, spy, qqq, dia


def polygon_spy_data():
    ''' Plotting the SPX Data '''
    key = "_t__ozhe3p5ACaYlHpPk2y4oEj7KkElP"
    with RESTClient(key) as client:
        l = ['SPY', 'QQQ']
        df = pd.DataFrame(columns=['Symbol', 'Close', 'Open', 'High', 'Low'])
    from_ = '2020-06-27'
    today = date.today()
    to = today.strftime("%Y-%m-%d")
    spy_list = list()
    meta = []
    value_spy = []
    resp = client.stocks_equities_aggregates('SPY', 1, "day", from_, to, unadjusted=False)
    for result in resp.results:
        dt = RESTClient.ts_to_datetime(result["t"])
        jmsg = {'time': dt, 'open': str(result['o']), 'high': str(result['h']), 'low': str(result['l']), 'close': str(result['c'])}
        spy_list.append(jmsg.copy())
        meta.append(str(dt))
        value_spy.append(result['c'])
    
    max_spy = max(value_spy)
    min_spy = min(value_spy)

    return meta, value_spy, max_spy, min_spy, spy_list


def spy_data_week():
    ''' Plotting the SPX Data '''

    key = "_t__ozhe3p5ACaYlHpPk2y4oEj7KkElP"
    with RESTClient(key) as client:
        l = ['SPY', 'QQQ']
        df = pd.DataFrame(columns=['Symbol', 'Close', 'Open', 'High', 'Low'])

    today = date.today()
    from_ = today - timedelta(days=today.weekday())
    to = today.strftime("%Y-%m-%d")
    spy_list = list()
    meta = []
    value_spy_week = []
    resp = client.stocks_equities_aggregates('SPY', 1, "day", from_, to, unadjusted=False)
    for result in resp.results:
        dt = RESTClient.ts_to_datetime(result["t"])
        jmsg = {'meta': dt, 'value': str(result['c'])}
        spy_list.append(jmsg.copy())
        meta.append(str(dt))
        value_spy_week.append(result['c'])

    max_spy = max(value_spy_week)
    min_spy = min(value_spy_week)

    print(value_spy_week)
    return value_spy_week, max_spy, min_spy

def polygon_qqq_data():
    ''' Plotting the QQQ Data '''

    key = "_t__ozhe3p5ACaYlHpPk2y4oEj7KkElP"
    with RESTClient(key) as client:
        l = ['QQQ', 'SPY']
        df = pd.DataFrame(columns=['Symbol', 'Close', 'Open', 'High', 'Low'])
    from_ = '2020-06-27'
    today = date.today()
    to = today.strftime("%Y-%m-%d")
    qqq_list = list()
    meta = []
    value_qqq = []
    resp = client.stocks_equities_aggregates('QQQ', 1, "day", from_, to, unadjusted=False)
    for result in resp.results:
        dt = RESTClient.ts_to_datetime(result["t"])
        jmsg = {'time': dt, 'open': str(result['o']), 'high': str(result['h']), 'low': str(result['l']), 'close': str(result['c'])}
        qqq_list.append(jmsg.copy())
        meta.append(str(dt))
        value_qqq.append(result['c'])

    max_qqq = max(value_qqq)
    min_qqq = min(value_qqq)

    return value_qqq, max_qqq, min_qqq, qqq_list



def polygon_crypto_values():
    """ Polygon (Crypto) REST API Implementation """

    key = "_t__ozhe3p5ACaYlHpPk2y4oEj7KkElP"
    with RESTClient(key) as client:
        l = ['X:BTCUSD', 'X:ETHUSD']
        df = pd.DataFrame(columns=['Symbol', 'Close', 'Open', 'High', 'Low'])
        for i in l:
            resp = client.crypto_previous_close(i)
            for result in resp.results:
                close = result['c']
                open = result['o']
                high = result['h']
                low = result['l']
            row = {'Symbol': i, 'Close': close, 'Open': open, 'High': high, 'Low': low}
            df = df.append(row, ignore_index=True)
        df = df.set_index('Symbol')

        btc = df.loc['X:BTCUSD', 'Close']
        eth = df.loc['X:ETHUSD', 'Close']
        v_btc = round(df.loc['X:BTCUSD', 'High'] - df.loc['X:BTCUSD', 'Low'], 2)
        v_eth = round(df.loc['X:ETHUSD', 'High'] - df.loc['X:ETHUSD', 'Low'], 2)

        return btc, eth, v_btc, v_eth


def polygon_btc_data():
    ''' Plotting the Bitcoin Data '''
    key = "_t__ozhe3p5ACaYlHpPk2y4oEj7KkElP"
    with RESTClient(key) as client:
        from_ = '2021-01-01'
        today = date.today()
        to = today.strftime("%Y-%m-%d")
        btc_list = list()
        meta = []
        value_btc = [] 
        resp = client.crypto_aggregates('X:BTCUSD', 1, "day", from_, to, unadjusted=False)
        for result in resp.results:
            dt = RESTClient.ts_to_datetime(result["t"])
            jmsg = {'time': dt, 'open': str(result['o']), 'high': str(result['h']), 'low': str(result['l']), 'close': str(result['c'])}
            btc_list.append(jmsg.copy())
            meta.append(dt)
            value_btc.append(result['c'])

        max_btc = max(value_btc)
        min_btc = min(value_btc)

    return value_btc, max_btc, min_btc, btc_list


def polygon_eth_data():
    ''' Plotting the Etherum Data '''
    key = "_t__ozhe3p5ACaYlHpPk2y4oEj7KkElP"
    with RESTClient(key) as client:
        from_ = '2021-01-01'
        today = date.today()
        to = today.strftime("%Y-%m-%d")
        eth_list = list()
        meta = []
        value_eth = []
        resp = client.crypto_aggregates('X:ETHUSD', 1, "day", from_, to, unadjusted=False)
        for result in resp.results:
            dt = RESTClient.ts_to_datetime(result["t"])
            jmsg = {'time': dt, 'open': str(result['o']), 'high': str(result['h']), 'low': str(result['l']), 'close': str(result['c'])}
            eth_list.append(jmsg.copy())
            meta.append(dt)
            value_eth.append(result['c'])

        max_eth = max(value_eth)
        min_eth = min(value_eth)

    return value_eth, max_eth, min_eth, eth_list


def ts_to_datetime(ts) -> str:
    return datetime.datetime.fromtimestamp(ts / 1000.0).strftime('%Y-%m-%d %H:%M')


def polygon_news_feed():
    key = "_t__ozhe3p5ACaYlHpPk2y4oEj7KkElP"
    # RESTClient can be used as a context manager to facilitate closing the underlying http session
    # https://requests.readthedocs.io/en/master/user/advanced/#session-objects
    with RESTClient(key) as client:
        df = pd.DataFrame(columns=['Title', 'Time', 'URL', 'ticker'])
        resp = client.reference_ticker_news_v2()
        for result in resp.results:
            publisher = result['publisher']
            time = result['published_utc']
            jmsg = {'Title': result['title'],
                    'Time': time[11:16],
                    'URL': publisher['name'],
                    'ticker': result['tickers']}

            df = df.append(jmsg, ignore_index=True)

    headline_1 = df.loc[0, 'Title']
    headline_2 = df.loc[1, 'Title']
    headline_3 = df.loc[2, 'Title']
    headline_4 = df.loc[3, 'Title']
    headline_5 = df.loc[4, 'Title']

    ticker_1 = df.loc[0, 'ticker']
    ticker_2 = df.loc[1, 'ticker']
    ticker_3 = df.loc[2, 'ticker']
    ticker_4 = df.loc[3, 'ticker']
    ticker_5 = df.loc[4, 'ticker']

    utc_1 = df.loc[0, 'Time']
    utc_2 = df.loc[1, 'Time']
    utc_3 = df.loc[2, 'Time']
    utc_4 = df.loc[3, 'Time']
    utc_5 = df.loc[4, 'Time']

    source_1 = df.loc[0, 'URL']
    source_2 = df.loc[1, 'URL']
    source_3 = df.loc[2, 'URL']
    source_4 = df.loc[3, 'URL']
    source_5 = df.loc[4, 'URL']

    return headline_1, headline_2, headline_3, headline_4, headline_5, ticker_1, ticker_2, ticker_3, ticker_4, \
           ticker_5, utc_1, utc_2, utc_3, utc_4, utc_5, source_1, source_2, source_3, source_4, source_5

def get_data(symbol):
    key = "_t__ozhe3p5ACaYlHpPk2y4oEj7KkElP"

    # RESTClient can be used as a context manager to facilitate closing the underlying http session
    with RESTClient(key) as client:
        from_ = "2020-11-01"
        today = date.today()
        to = today.strftime("%Y-%m-%d")
        yesterday = today - datetime.timedelta(days=1)
        resp = client.stocks_equities_aggregates(symbol, 1, "day", from_, yesterday, unadjusted=False)

        df = pd.DataFrame(columns=['Date', 'Open', 'Close', 'High', 'Low', 'Volume'])

        for result in resp.results:
            dt = ts_to_datetime(result["t"])
            l = {'Date': dt, 'Open': result['o'], 'Close': result['c'], 'High': result['h'], 'Low': result['l'],
                 'Volume': result['v']}
            df = df.append(l, ignore_index=True)

    return df

def breakout():


    stocks = ['AAPL', 'MSFT', 'GOOG', 'GOOGL', 'AMZN', 'FB', 'TSLA', 'BRK.B', 'NVDA', 'V', 'JPM', 'JNJ', 'WMT', 'UNH', 'HD', 'PG', 'MA', 'BAC', 'DIS', 'PYPL', 'ADBE', 'CMCSA', 'NFLX', 'CRM', 'PFE', 'NKE', 'ORCL', 'CSCO', 'KO', 'TMO', 'DHR', 'XOM', 'VZ', 'LLY', 'ACN', 'ABT', 'INTC', 'PEP', 'AVGO', 'COST', 'T', 'WFC', 'ABBV', 'CVX', 'MRK', 'MS', 'MCD', 'TXN', 'MDT', 'MRNA', 'UPS', 'NEE', 'PM', 'TMUS', 'LIN', 'INTU', 'QCOM', 'HON', 'LOW', 'CHTR', 'C', 'BMY', 'AMT', 'SBUX', 'BLK', 'SCHW', 'UNP', 'NOW', 'AXP', 'GS', 'RTX', 'AMD', 'BA', 'AMAT', 'AMGN', 'ISRG', 'IBM', 'TGT', 'EL', 'CVS', 'GE', 'SPGI', 'DE', 'CAT', 'MMM', 'SYK', 'BKNG', 'PLD', 'ZTS', 'LMT', 'ANTM', 'GILD', 'MO', 'MDLZ', 'ADP', 'LRCX', 'TJX', 'USB', 'HCA', 'MU', 'CCI', 'MMC', 'PNC', 'CB', 'SHW', 'DUK', 'COP', 'EQIX', 'FIS', 'BDX', 'EW', 'TFC', 'GM', 'FISV', 'COF', 'CI', 'MCO', 'ITW', 'SO', 'CME', 'REGN', 'CSX', 'FDX', 'ICE', 'AON', 'WM', 'ILMN', 'CL', 'ETN', 'ADI', 'ADSK', 'BSX', 'ECL', 'NSC', 'D', 'ATVI', 'APD', 'EMR', 'IDXX', 'ALGN', 'NOC', 'PSA', 'KLAC', 'GD', 'DXCM', 'PGR', 'NXPI', 'CMG', 'MSCI', 'HUM', 'A', 'JCI', 'DG', 'INFO', 'MET', 'F', 'MNST', 'SNPS', 'ROP', 'TWTR', 'EXC', 'FTNT', 'IQV', 'VRTX', 'EBAY', 'GPN', 'CARR', 'TROW', 'MAR', 'TEL', 'FCX', 'AIG', 'KMB', 'LHX', 'CDNS', 'BIIB', 'DLR', 'APH', 'KHC', 'TT', 'NEM', 'MCHP', 'BK', 'SPG', 'DOW', 'WBA', 'SRE', 'EOG', 'AEP', 'RMD', 'ORLY', 'BAX', 'CTAS', 'STZ', 'ROST', 'MSI', 'CTSH', 'RSG', 'PAYX', 'SYY', 'APTV', 'SBAC', 'ALL', 'PRU', 'SLB', 'TRV', 'CNC', 'YUM', 'XLNX', 'EA', 'PH', 'MPC', 'PXD', 'WELL', 'HSY', 'DFS', 'HLT', 'GIS', 'KMI', 'DD', 'OTIS', 'MTD', 'ROK', 'AFL', 'PPG', 'XEL', 'AZO', 'TDG', 'ADM', 'ODFL', 'IFF', 'CPRT', 'FRC', 'SIVB', 'WST', 'BF.B', 'VRSK', 'AWK', 'GLW', 'GRMN', 'EFX', 'KEYS', 'NDAQ', 'CMI', 'CBRE', 'DHI', 'HPQ', 'PEG', 'MCK', 'ANSS', 'AVB', 'CTVA', 'FAST', 'WMB', 'BLL', 'AJG', 'EQR', 'LEN', 'ZBH', 'LYB', 'KR', 'SWK', 'ARE', 'AME', 'ZBRA', 'LUV', 'WLTW', 'AMP', 'PAYC', 'LVS', 'WEC', 'ES', 'NUE', 'LH', 'STT', 'PSX', 'SWKS', 'PCAR', 'TSN', 'ETSY', 'ANET', 'SYF', 'WY', 'FITB', 'GNRC', 'VFC', 'O', 'BBY', 'DAL', 'IT', 'ED', 'CDW', 'VLO', 'FTV', 'CCL', 'ABC', 'VIAC', 'ALB', 'KSU', 'WAT', 'EXR', 'VRSN', 'URI', 'OXY', 'HIG', 'BKR', 'OKE', 'XYL', 'TSCO', 'DOV', 'BIO', 'CTLT', 'COO', 'MKC', 'HRL', 'KMX', 'VMC', 'MPWR', 'TRMB', 'CZR', 'EXPE', 'IR', 'DISH', 'DTE', 'NTRS', 'PPL', 'ETR', 'EIX', 'IP', 'CRL', 'CERN', 'MAA', 'K', 'VTR', 'AEE', 'MLM', 'HBAN', 'STE', 'RCL', 'FLT', 'GWW', 'HES', 'ESS', 'FOX', 'FOXA', 'TECH', 'PKI', 'EXPD', 'CHD', 'ENPH', 'CLX', 'ULTA', 'NTAP', 'MGM', 'FE', 'DLTR', 'TDY', 'HOLX', 'DRI', 'TER', 'KEY', 'BR', 'DVN', 'LYV', 'QRVO', 'STX', 'DGX', 'TYL', 'PEAK', 'DRE', 'POOL', 'CINF', 'DPZ', 'RF', 'ROL', 'AMCR', 'CFG', 'RJF', 'CMS', 'JBHT', 'TFX', 'NVR', 'AKAM', 'AVY', 'WDC', 'HAL', 'HPE', 'TTWO', 'GPC', 'MTB', 'BXP', 'BBWI', 'INCY', 'J', 'PFG', 'WAB', 'IEX', 'PWR', 'MKTX', 'CE', 'VTRS', 'CAG', 'AES', 'UDR', 'ABMD', 'TXT', 'OMC', 'BEN', 'EVRG', 'NLOK', 'LKQ', 'CNP', 'UAL', 'CAH', 'LNT', 'FANG', 'IPG', 'PTC', 'LUMN', 'MAS', 'CTXS', 'EMN', 'L', 'PKG', 'HWM', 'SJM', 'AAL', 'HAS', 'KIM', 'WHR', 'DISCA', 'DISCK', 'LDOS', 'XRAY', 'WRK', 'CBOE', 'CPB', 'FBHS', 'IRM', 'AAP', 'NWS', 'NWSA', 'WRB', 'MHK', 'DVA', 'JKHY', 'PNR', 'ALLE', 'PHM', 'UHS', 'MOS', 'FFIV', 'FMC', 'LNC', 'ATO', 'HST', 'PENN', 'REG', 'CHRW', 'SNA', 'RHI', 'IVZ', 'TPR', 'HSIC', 'AOS', 'CF', 'NWL', 'NRG', 'RE', 'BWA', 'TAP', 'CMA', 'WYNN', 'NI', 'AIZ', 'FRT', 'MRO', 'ZION', 'GPS', 'JNPR', 'GL', 'LW', 'DXC', 'UA', 'UAA', 'IPGP', 'SEE', 'OGN', 'WU', 'PNW', 'RL', 'VNO', 'HII', 'COG', 'PVH', 'APA', 'ALK', 'NLSN', 'HBI', 'LEG', 'PRGO', 'NCLH', 'NOV', 'UNM']

    buy_list = []
    consolidation_price = []

    stock_buy = []

    for i in stocks:
        df = get_data(i)
        df1 = df[0:-30]
        a = len(df) - 1
        consolidation = max(df1['Close'])

        if df.loc[a, 'Close'] > (consolidation + (.15 * consolidation)):
            buy_list.append(False)
        elif df.loc[a, 'Close'] in range(int(consolidation + (.01 * consolidation)),
                                         int(consolidation + (.05 * consolidation))):
            buy_list.append(True)
            stock_buy.append(i)
            consolidation_price.append(consolidation)
        else:
            buy_list.append(False)

    sdict = {'Stocks': stock_buy,
             'Pivot': consolidation_price}


    breakout_stocks = sdict['Stocks']
    Pivot = sdict['Pivot']
    print(breakout_stocks)
    return breakout_stocks, Pivot

def polygon_crypto_data(request):
    ''' Plotting the Crypto Data '''
    if(request.method == 'POST'):
        data = json.loads(request.body.decode('utf-8'))['data']
        key = "_t__ozhe3p5ACaYlHpPk2y4oEj7KkElP"
        with RESTClient(key) as client:
            from_ = data["startDate"]
            today = date.today()
            to = today.strftime("%Y-%m-%d")
            crypto= "X:{c}USD".format(c=data["cryptoCode"])
            crypto_list = list()
            resp = client.crypto_aggregates(crypto, 1, "day", from_, to, unadjusted=False)
            for result in resp.results:
                dt = RESTClient.ts_to_datetime(result["t"])
                jmsg = {'time': dt, 'value': result['c']}
                crypto_list.append(jmsg.copy())

        if (crypto_list):
            return JsonResponse({"status": 0, "data": {"cryptoValues": json.dumps(crypto_list)}})
        else:
            return JsonResponse({"status": 1, "message": "Error in fetching crypto data !"})

''' Fundamental Analysis & Modelling
 
 Fundamental analysis fetches stock financials data from polygon 
 using stock_financials API function. This data is than parsed and 
 statistical analysis is being performed 
'''


