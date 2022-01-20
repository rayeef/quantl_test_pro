''' this module connects to polygon rest and output dataframe for given ticker (tickers) '''
import warnings
warnings.filterwarnings('ignore')
from polygon_api.polygon_rest import RESTClient
import pandas as pd
from sklearn.feature_selection import mutual_info_regression
from alpha_wrapper import BaseAlpha
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt



class LoadData:
    def __init__(self,symbol):
        key = "_t__ozhe3p5ACaYlHpPk2y4oEj7KkElP"
        with RESTClient(key) as client:
            start = "2007-01-01"
            end = "2021-10-05"
            resp = client.stocks_equities_aggregates(symbol, 1, "day", start, end, unadjusted=False)
            df = pd.DataFrame(columns=['Date', 'Open', 'Close', 'High', 'Low', 'Volume', 'VWAP'])


            for result in resp.results:
                dt = RESTClient.ts_to_datetime(result["t"])
                l = {'Date': dt, 'Open': result['o'], 'Close': result['c'], 'High': result['h'], 'Low': result['l'],
                     'Volume': result['v'], 'VWAP': result['vw']}
                df = df.append(l, ignore_index=True)

                ''' Data specific parameters calculations '''
                returns = df['Close'].pct_change()
                fwd_return = ((1 / len(returns)) * returns).cumsum()
                adv20 = df['Volume'].rolling(20).mean().reset_index(0, drop=True)
                '''Append in main Dataframe '''
                df = df.assign(adv20=adv20, returns=returns, fwd_return=fwd_return)

        df = df.join(df.groupby('Date')['Open', 'Close', 'High', 'Low', 'Volume'].rank(axis=1, pct=True),
                     rsuffix='_rank')
        self.df = df
        print(df.info(show_counts=True))
        self.df = df
        self.b = BaseAlpha(df,window=10, period=10)
        '''For dev purpose only'''
        #show(df)

    def fwd_returns(self):
        df = self.df
        returns = df['returns']
        fwd_return = ((1 / len(returns)) * returns).cumsum()
        '''this function to calculate forward returns will be implemented later'''
        return fwd_return

    def get_mutual_info_score(returns, alpha, n=100):
        df = pd.DataFrame({'y': returns, 'alpha': alpha}).dropna().sample(n=n)
        return mutual_info_regression(y=df.y, X=df[['alpha']])[0]

    def alpha001(self):

        '''rank(ts_argmax(power(((returns < 0) ? ts_std(returns, 20) : close), 2.), 5))'''
        df = self.df
        wrap = self.b

        c = df['Close']
        r = df['returns']
        c[r < 0] = wrap.ts_std(r, 20)
        alpha001 = np.stack(wrap.rank(wrap.ts_argmax(wrap.power(c,2), 5)).mul(-.5))
        df = df.assign(alpha001=alpha001)

        '''plotting & post analysis '''
        alphas = df[['returns', 'fwd_return', 'alpha001']].copy()
        print(alphas.info())
        g = sns.jointplot(x='alpha001', y='fwd_return', data=alphas)
        plt.show()

        '''Mutual Info Score '''
        mi = LoadData.get_mutual_info_score(alphas.fwd_return, alphas.alpha001)
        return mi

    def alpha002(self):

        '''correlation(rank(delta(log(volume), 2)), rank(((close - open) / open)), 6)'''
        df = self.df
        wrap = self.b

        o = df['Open']
        c = df['Close']
        v = df['Volume'].apply(lambda x: float(x))


        s1 = wrap.rank(wrap.ts_delta(wrap.log(v), 2))
        s2 = wrap.rank((c/o)-1)
        alpha002 = -wrap.ts_corr(s1, s2, 6)

        df = df.assign(alpha002=alpha002)
        '''plotting & post analysis '''
        alphas = df[['returns', 'fwd_return', 'alpha002']].copy()
        print(alphas.info())
        g = sns.jointplot(x='alpha002', y='fwd_return', data=alphas)
        g.plot_joint(sns.kdeplot, color="r", zorder=0, levels=6)
        g.plot_marginals(sns.rugplot, color="r", height=-.15, clip_on=False)
        plt.show()

        '''Mutual Info Score '''
        mi = LoadData.get_mutual_info_score(alphas.fwd_return, alphas.alpha002)
        return mi

