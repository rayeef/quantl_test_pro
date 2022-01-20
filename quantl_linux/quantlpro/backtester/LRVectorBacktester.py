'''python module for vectorized backtesting strategy inspired by linear Regression '''

import numpy as np
import pandas as pd
from polygon_api.polygon_rest import RESTClient


class LRVectorBacktester(object):
        '''
        Class for the vectorized backtesting of
        linear regression-based trading strategies.

        Attributes
        ==========
        symbol: str
           TR RIC (financial instrument) to work with
        start: str
            start date for data selection
        end: str
            end date for data selection
        amount: int, float
            amount to be invested at the beginning
        tc: float
            proportional transaction costs (e.g., 0.5% = 0.005) per trade

        Methods
        =======
        get_data:
            retrieves and prepares the base data set
        select_data:
            selects a sub-set of the data
        prepare_lags:
            prepares the lagged data for the regression
        fit_model:
            implements the regression step
        run_strategy:
            runs the backtest for the regression-based strategy
        plot_results:
            plots the performance of the strategy compared to the symbol
        '''
def __init__(self, symbol, start, end, amount, tc):
        self.symbol = symbol
        self.start = start
        self.end = end
        self.amount = amount
        self.tc = tc
        self.results = None
        self.get_data()

def get_data(self):
    '''Retrieves & Prepares the data'''
    # data = FetchData.main()
    key = "_t__ozhe3p5ACaYlHpPk2y4oEj7KkElP"

    # RESTClient can be used as a context manager to facilitate closing the underlying http session
    # https://requests.readthedocs.io/en/master/user/advanced/#session-objects
    with RESTClient(key) as client:

        resp = client.stocks_equities_aggregates(self.symbol, 1, "day", self.start, self.end, unadjusted=False)

        print(f"Daily aggregates for {resp.ticker} between {self.start} and {self.end}.")
        df = pd.DataFrame(columns=['Date', 'Open', 'Close', 'High', 'Low', 'Volume'])
        for result in resp.results:
            dt = RESTClient.ts_to_datetime(result["t"])
            l = {'Date': dt, 'Open': result['o'], 'Close': result['c'], 'High': result['h'], 'Low': result['l'],
                 'Volume': result['v']}
            df = df.append(l, ignore_index=True)

    df['return'] = np.log(df['Close'] / df['Close'].shift(1))
    self.data = df.dropna()


def select_data(self, start, end):
        ''' Selects sub-sets of the financial data. '''
        data = self.data[(self.data.index >= start) &
                         (self.data.index <= end)].copy()
        return data

def prepare_lags(self, start, end):
        ''' this function prepares the lagged data for predictions and regression '''
        data = self.select_data(start, end)
        self.cols = []
        for lag in range(1, self.lags + 1):
            col = f'lag_{lag}'
            data[col] = data['return'].shift(lag)
            self.cols.append(col)
        data.dropna(inplace=True)
        self.lagged_data = data

def fit_model(self, start, end):
        ''' function implements regression step '''
        self.prepare_lags(start, end)
        reg = np.linalg.lstsq(self.lagged_data[self.cols], np.sign(self.lagged_data['return']), rcond=None)[0]
        self.reg = reg

def run_strategy(self, start_in, end_in, start_out, end_out, lags=3):
        ''' Backtests the trading strategy.
        '''
        self.lags = lags
        self.fit_model(start_in, end_in)
        self.results = self.select_data(start_out, end_out).iloc[lags:]
        self.prepare_lags(start_out, end_out)
        prediction = np.sign(np.dot(self.lagged_data[self.cols], self.reg))
        self.results['prediction'] = prediction
        self.results['strategy'] = self.results['prediction'] * \
                                   self.results['returns']
        # determine when a trade takes place
        trades = self.results['prediction'].diff().fillna(0) != 0
        # subtract transaction costs from return when trade takes place
        self.results['strategy'][trades] -= self.tc
        self.results['creturns'] = self.amount * \
                                   self.results['returns'].cumsum().apply(np.exp)
        self.results['cstrategy'] = self.amount * \
                                    self.results['strategy'].cumsum().apply(np.exp)
        # gross performance of the strategy
        aperf = self.results['cstrategy'].iloc[-1]
        # out-/underperformance of strategy
        operf = aperf - self.results['creturns'].iloc[-1]
        return round(aperf, 2), round(operf, 2)

def plot_results(self):
        ''' Plots the cumulative performance of the trading strategy
        compared to the symbol.
        '''
        if self.results is None:
            print('No results to plot yet. Run a strategy.')
        title = '%s | TC = %.4f' % (self.symbol, self.tc)
        self.results[['creturns', 'cstrategy']].plot(title=title,
                                                     figsize=(10, 6))



# if __name__ == '__main__':
#     lrbt = LRVectorBacktester("MSFT","2010-01-01","2018-01-01", 10000, 0.0)
#     '''Trains and evaluates the strategy on the same data set.'''
#     print(lrbt.run_strategy("2010-01-01", "2019-01-01",
#                             "2010-01-01", "2019-01-01"))
#    ''' Uses two different data sets for the training and evaluation steps.'''
#     print(lrbt.run_strategy("2010-01-01", "2019-01-01",
#                             "2019-01-01", "2020-01-01"), lags=5)
