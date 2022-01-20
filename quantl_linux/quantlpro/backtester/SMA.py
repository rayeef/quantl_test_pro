import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import time
import io
import datetime
import pandas as pd
from polygon_api.polygon_rest import RESTClient
from scipy.optimize import brute



class SMA(object):
    def __init__(self,symbol, _from,to, fast, slow):
        self.symbol = symbol
        self._from = _from
        self.to = to
        self.fast = fast
        self.slow = slow
        self.results = None
        self.get_data()

    def ts_to_datetime(self,ts) -> str:
        return datetime.datetime.fromtimestamp(ts / 1000.0).strftime('%Y-%m-%d %H:%M')

    def get_data(self):
        #data = FetchData.main()
        key = "_t__ozhe3p5ACaYlHpPk2y4oEj7KkElP"

        # RESTClient can be used as a context manager to facilitate closing the underlying http session
        # https://requests.readthedocs.io/en/master/user/advanced/#session-objects
        with RESTClient(key) as client:
            from_ = "2010-01-01"
            to = "2021-09-09"
            resp = client.stocks_equities_aggregates(self.symbol, 1, "day", self._from, self.to, unadjusted=False)

            print(f"Minute aggregates for {resp.ticker} between {from_} and {to}.")
            df = pd.DataFrame(columns=['Date', 'Open', 'Close', 'High', 'Low', 'Volume'])
            for result in resp.results:
                dt = RESTClient.ts_to_datetime(result["t"])
                # print(f"{dt}\n\tO: {result['o']}\n\tH: {result['h']}\n\tL: {result['l']}\n\tC: {result['c']} ")
                l = {'Date': dt, 'Open': result['o'], 'Close': result['c'], 'High': result['h'], 'Low': result['l'],
                     'Volume': result['v']}
                df = df.append(l, ignore_index=True)
                '''printing dataframe for internal debugging only'''
                #print(df)
        self.data = df

    def set_parameters(self, fast=None, slow=None):
        ''' Updates SMA parameters and resp. time series.
        '''
        if fast is not None:
            self.fast = fast
            self.data['fast'] = self.data['price'].rolling(
                self.fast).mean()
        if slow is not None:
            self.slow = slow
            self.data['slow'] = self.data['price'].rolling(self.slow).mean()

    def run_strategy(self):
        data = self.data.copy().dropna()

        data['Fast MA'] = data['Close'].rolling(window=self.fast).mean()
        data['Slow MA'] = data['Close'].rolling(window=self.slow).mean()
        data['Crossover'] = data['Fast MA'] - data['Slow MA']
        data['Signal'] = np.where(data['Crossover'] > 0, 1, -1)

        # sb.lineplot(data['Date'],data['Crossover'])
        # sb.lineplot(x='Date',y='Signal',data=data)
        # data.plt(x='Date',y='Signal')
        # plt.plot(data['Date'],data['Signal'])
        # plt.yticks(np.arange(-1,2,1))
        # plt.show()

        data['rs'] = data['Close'].apply(np.log).diff(1)
        data['my_rs'] = data['rs'].shift(1)
        data['exp_data'] = data['my_rs'].cumsum().apply(np.exp)

        # sb.lineplot(data['Date'],data['exp_data'])

        data['returns'] = np.log(data['Close'] / data['Close'].shift(1))
        # data['returns'].hist(bins=35, figsize=(10, 6))
        data['strategy_return'] = data['Signal'].shift(1) * data['returns']

        print(data[['returns', 'strategy_return']].sum())
        print("gross performance = ", data[['returns', 'strategy_return']].sum().apply(np.exp))

        data[['returns', 'strategy_return']].cumsum(
                         ).apply(np.exp).plot(figsize=(10, 6))


        # Gross performance over time =>
        data['cumret'] = data['strategy_return'].cumsum().apply(np.exp)
        print(data['cumret'].dropna())
        # Max value of gross performance =>
        data['cummax'] = data['cumret'].cummax()

        # data[['cumret', 'cummax']].dropna().plot(figsize=(10, 6))
        drawdown_column = data['cummax'] - data['cumret']
        drawdown_column.max()

        self.results = data


    def get_results(self):
        data = self.results

        if self.results is None:
            print('No results to plot yet. Run a strategy.')
        else:
            print('Generating results.......')

        # assigning variables
        a = str(data[['returns', 'strategy_return']].sum())
        b = str(data[['returns', 'strategy_return']].sum().apply(np.exp))

        ts = time.time()
        timestamp = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d_%H-%M-%S')
        data['Date'] = pd.to_datetime(data['Date'])
        datemin = np.datetime64(data['Date'][0])
        datemax = np.datetime64(data['Date'].iloc[-1])




        fig = plt.figure()
        axis1 = fig.add_subplot(211)
        axis1.plot(data[['cumret', 'cummax']].dropna())
        axis1.set_title("Cumulative Performance")
        fig.tight_layout(pad=1.5)
        axis2 = fig.add_subplot(212)
        axis2.plot(data[['returns', 'strategy_return']].cumsum().apply(np.exp))
        axis2.legend(['Equity return', 'Strategy return'], title='Legend')
        axis2.set_title("Gross Performance")



        # move to the beginning of the StringIO buffer

        fig, axs = plt.subplots(2, 2)
        axs[0, 0].plot(data['Date'], data['Crossover'])
        axs[0, 0].set_title("SMA Crossover")
        axs[1, 0].plot(data['Date'], data['Signal'])
        axs[1, 0].set_title("Position Signal")
        axs[1, 0].sharex(axs[0, 0])
        axs[0, 1].plot(data[['cumret', 'cummax']].dropna())
        axs[0, 1].set_title("Cumulative Performance")
        axs[1, 1].plot(data[['returns', 'strategy_return']].cumsum().apply(np.exp))
        axs[1, 1].set_title("Gross Performance ")
        fig.tight_layout()
        plt.show()






sma =  SMA("SPY","2019-04-01","2021-10-09",21,50)
sma.run_strategy()
sma.get_results()

