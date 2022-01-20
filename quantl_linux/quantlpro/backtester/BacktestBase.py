'''Base classs for Backtesting - drived from Event Driven Back testing strategy '''



import pandas as pd
import numpy as np
from pylab import mpl, plt
plt.style.use('seaborn')
mpl.rcParams['font.family'] = 'serif'
import datetime
from datetime import date
from polygon_api.polygon_rest import RESTClient
import quantlplot as qplt


class BacktestBase(object):
    ''' Base class for event-based backtesting of trading strategies.

        Attributes
        ==========
        symbol: str
            TR RIC (financial instrument) to be used
        start: str
            start date for data selection
        end: str
            end date for data selection
        amount: float
            amount to be invested either once or per trade
        ftc: float
            fixed transaction costs per trade (buy or sell)
        ptc: float
            proportional transaction costs per trade (buy or sell)

        Methods
        =======
        get_data:
            retrieves and prepares the base data set
        plot_data:
            plots the closing price for the symbol
        get_date_price:
            returns the date and price for the given bar
        print_balance:
            prints out the current (cash) balance
        print_net_wealth:
            prints out the current net wealth
        place_buy_order:
            places a buy order
        place_sell_order:
            places a sell order
        close_out:
            closes out a long or short position
        '''
    def __init__(self, symbol, start, end, amount,
                 ftc=0.0, ptc=0.0, verbose=True):
        self.symbol = symbol
        self.start = start
        self.end = end
        self.initial_amount = amount
        self.amount = amount
        self.ftc = ftc
        self.ptc = ptc
        self.SMA1 = 0
        self.SMA2 = 0
        self.units = 0
        self.position = 0
        self.trades = 0
        self.verbose = verbose
        self.get_data()

    def get_data(self):
        '''Retrives & prepares the data.
        '''
        key = "_t__ozhe3p5ACaYlHpPk2y4oEj7KkElP"
        # RESTClient can be used as a context manager to facilitate closing the underlying http session
        # https://requests.readthedocs.io/en/master/user/advanced/#session-objects
        with RESTClient(key) as client:
            from_ = "2010-01-01"
            today = date.today()
            to = today.strftime("%Y-%m-%d")
            resp = client.stocks_equities_aggregates(self.symbol, 1, "day", self.start, self.end, unadjusted=False)
            df = pd.DataFrame(columns=['Date', 'Open', 'Close', 'High', 'Low', 'Volume'])
            for result in resp.results:
                dt = RESTClient.ts_to_datetime(result["t"])
                l = {'Date': dt, 'Open': result['o'], 'Close': result['c'], 'High': result['h'], 'Low': result['l'],
                     'Volume': result['v']}
                df = df.append(l, ignore_index=True)
        df = df.astype({'Date' : 'datetime64[ns]'})
        self.data = df


    def plot_data(self):
        ''' Plots the closing prices for symbol.
        '''
        ax = qplt.create_plot(self.symbol, rows=1)
        candles = self.data[['Date', 'Open', 'Close', 'High', 'Low']]
        qplt.candlestick_ochl(candles)
        volume_plot = self.data[['Date', 'Open', 'Close', 'Volume']]
        qplt.volume_ocv(volume_plot, ax=ax.overlay())
        # restore view (X-position and zoom) if we ever run this example again
        # put an MA on the close price
        qplt.plot(self.data['Date'], self.data['SMA1'], ax=ax, legend='SMA1')
        qplt.plot(self.data['Date'], self.data['SMA2'], ax=ax, legend='SMA2')
        # place some dumb markers on low wicks
        df = self.data.dropna()
        df = df.reset_index()
        data = df
        df1 = pd.DataFrame()
        for i in range(len(data)):
            if (round(data.loc[i, 'SMA1']) == round(data.loc[i, 'SMA2'])):
                df1 = df1.append(data.loc[i], ignore_index=True)
        df1 = df1[['Date', 'Close']]
        qplt.plot(df1['Date'], df1['Close'], s=1500, ax=ax, color='#4a5', style='^', legend='Cross Over Signal')
        qplt.autoviewrestore()
        qplt.show()



    def get_date_price(self, bar):
        ''' Return date and price for bar.
        '''
        date = str(self.data.index[bar])[:10]
        price = self.data.Close.iloc[bar]
        return date, price

    def print_balance(self, bar):
        ''' Print out current cash balance info.
        '''
        date, price = self.get_date_price(bar)
        print(f'Bar:{date} | ${price:.2f} | Balance ${self.amount:.2f}')

    def print_net_wealth(self, bar):
        ''' Print out current cash balance info.
        '''
        date, price = self.get_date_price(bar)
        net_wealth = self.units * price + self.amount
        print(f'{date} | current net wealth {net_wealth:.2f}')

    def place_buy_order(self, bar, units=None, amount=None):
        ''' Place a buy order.
        '''
        date, price = self.get_date_price(bar)
        if units is None:
            units = int(amount / price)
        self.amount -= (units * price) * (1 + self.ptc) + self.ftc
        self.units += units
        self.trades += 1
        if self.verbose:
            print(f'{date} | selling {units} units at {price:.2f}')
            self.print_balance(bar)
            self.print_net_wealth(bar)

    def place_sell_order(self, bar, units=None, amount=None):
        ''' Place a sell order.
        '''
        date, price = self.get_date_price(bar)
        if units is None:
            units = int(amount / price)
        self.amount += (units * price) * (1 - self.ptc) - self.ftc
        self.units -= units
        self.trades += 1
        if self.verbose:
            print(f'{date} | selling {units} units at {price:.2f}')
            self.print_balance(bar)
            self.print_net_wealth(bar)

    def close_out(self, bar):
        ''' Closing out a long or short position.
        '''
        date, price = self.get_date_price(bar)
        self.amount += self.units * price
        self.units = 0
        self.trades += 1
        if self.verbose:
            print(f'{date} | inventory {self.units} units at {price:.2f}')
            print('=' * 55)
        print('Initial Deposit [$] {:.2f}'.format(self.initial_amount))
        print('Final balance   [$] {:.2f}'.format(self.amount))
        perf = ((self.amount - self.initial_amount) /
                self.initial_amount * 100)
        print('Net Performance [%] {:.2f}'.format(perf))
        print('Trades Executed [#] {:.2f}'.format(self.trades))
        business_days = (np.busday_count(self.start, self.end))
        print('Trading Days    [#] {:.2f}'.format(business_days))
        print('=' * 55)




