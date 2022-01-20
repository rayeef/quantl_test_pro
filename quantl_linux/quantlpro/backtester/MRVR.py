import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import time
import datetime
import matplotlib.dates as mdates
from matplotlib.backends.backend_pdf import PdfPages
from PyPDF2 import PdfFileWriter, PdfFileReader
import io
from datetime import date
from polygon_api.polygon_rest import RESTClient


# import seaborn as sb


class MRVR(object):
    def __init__(self,symbol, _from, to, sma, threshold, tc, amount):
        self.symbol = symbol
        self._from = _from
        self.to = to
        self.sma = sma
        self.threshold = threshold
        self.tc = tc
        self.amount = amount
        self.get_data()


    def get_data(self):
        # data = FetchData.main()
        key = "_t__ozhe3p5ACaYlHpPk2y4oEj7KkElP"

        # RESTClient can be used as a context manager to facilitate closing the underlying http session
        # https://requests.readthedocs.io/en/master/user/advanced/#session-objects
        with RESTClient(key) as client:
            from_ = "2010-01-01"
            today = date.today()
            to = today.strftime("%Y-%m-%d")
            resp = client.stocks_equities_aggregates(self.symbol, 1, "day", self._from, self.to, unadjusted=False)

            print(f"Minute aggregates for {resp.ticker} between {from_} and {to}.")
            df = pd.DataFrame(columns=['Date', 'Open', 'Close', 'High', 'Low', 'Volume'])
            for result in resp.results:
                dt = RESTClient.ts_to_datetime(result["t"])
                # print(f"{dt}\n\tO: {result['o']}\n\tH: {result['h']}\n\tL: {result['l']}\n\tC: {result['c']} ")
                l = {'Date': dt, 'Open': result['o'], 'Close': result['c'], 'High': result['h'], 'Low': result['l'],
                     'Volume': result['v']}
                df = df.append(l, ignore_index=True)

                # print(df)
        self.data = df

    def run_strategy(self):

        data = self.data
        data['sma'] = data['Close'].rolling(self.sma).mean()
        data['distance'] = data['Close'] - data['sma']
        data.dropna(inplace=True)
        data['return'] = np.log(data['Close'] / data['Close'].shift(1))
        # sell signals
        data['position'] = np.where(data['distance'] > self.threshold,
                                    -1, np.nan)
        # buy signals
        data['position'] = np.where(data['distance'] < -self.threshold,
                                    1, data['position'])

        # crossing of current price and SMA (zero distance)
        data['position'] = np.where(data['distance'] *
                                    data['distance'].shift(1) < 0,
                                    0, data['position'])

        data['position'] = data['position'].ffill().fillna(0)
        data['strategy'] = data['position'].shift(1) * data['return']

        # determine when a trade takes place
        trades = data['position'].diff().fillna(0) != 0

        # subtract transaction costs from return when trade takes place
        data['strategy'][trades] -= self.tc
        data['creturns'] = self.amount * \
                           data['return'].cumsum().apply(np.exp)
        data['cstrategy'] = self.amount * \
                            data['strategy'].cumsum().apply(np.exp)
        results = data
        # absolute performance of the strategy
        # aperf = results['cstrategy'].iloc[-1]
        # out-/underperformance of strategy
        # operf = aperf - results['creturns'].iloc[-1]
        # print(round(aperf, 2), round(operf, 2))
        self.results = results
        self.data = data

    def get_results(self):
        results = self.results
        if results is None:
            print('No results to plot yet. Run a strategy.')
        # assigning variables
        ts = time.time()
        timestamp = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d_%H-%M-%S')
        plot = str('p' + timestamp + '.pdf')
        # absolute performance of the strategy
        aperf = results['cstrategy'].iloc[-1]
        # out-/underperformance of strategy
        operf = aperf - results['creturns'].iloc[-1]
        a = str(round(aperf, 2))
        b = str(round(operf, 2))

        # printing plots
        pp = PdfPages(plot)
        fig, ax = plt.subplots()
        ax.plot(results[['creturns', 'cstrategy']])
        ax.legend(['Equity return', 'Strategy return'], title='Legend')
        ax.set_title('Gross Performance')
        fig.savefig(pp, format='pdf')


# -----remove before production---------------------------------
mrvr = MRVR("AAPL","2010-01-01","2021-09-09",42, 7.5, 0.0, 10000)
mrvr.run_strategy()
mrvr.get_results()
