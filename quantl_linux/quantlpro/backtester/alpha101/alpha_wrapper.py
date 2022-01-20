
import warnings
warnings.filterwarnings('ignore')

import numpy as np
import pandas as pd
#from talib import WMA

''' this is a base alphs class that contains mostly wrapper functions to be used in main Alpha101 class '''

class BaseAlpha:
    def __init__(self, df, window, period):
        self.df = df
        self.window = window
        self.period = period

    def rank(self, df):
        """Return the cross-sectional percentile rank
         Args:
             :param df: tickers in columns, sorted dates in rows.

         Returns:
             pd.DataFrame: the ranked values
         """
        return df.rank(axis=1, pct=True)

    def scale(self, df):
        """
        Scaling time serie.
        :param df: a pandas DataFrame.
        :param k: scaling factor.
        :return: a pandas DataFrame rescaled df such that sum(abs(df)) = k
        """
        return df.div(df.abs().sum(axis=1), axis=0)

    def log(self, df):
        return np.log1p(df)

    def sign(self, df):
        return np.sign(df)

    def power(self, df, exp):
        return df.pow(exp)

    ''' Time series wrappers ts__* '''

    def ts_lag(self, df: pd.DataFrame, t: int = 1) -> pd.DataFrame:
        """Return the lagged values t periods ago.
        Args:
            :param df: tickers in columns, sorted dates in rows.
            :param t: lag

        Returns:
            pd.DataFrame: the lagged values
        """
        return df.shift(t)

    def ts_delta(self, df, period=1):
        """
        Wrapper function to estimate difference.
        :param df: a pandas DataFrame.
        :param period: the difference grade.
        :return: a pandas DataFrame with today’s value minus the value 'period' days ago.
        """
        return df.diff(period)

    def ts_sum(self, df: pd.DataFrame, window: int = 10) -> pd.DataFrame:
        """Computes the rolling ts_sum for the given window size.

        Args:
            df (pd.DataFrame): tickers in columns, dates in rows.
            window      (int): size of rolling window.

        Returns:
            pd.DataFrame: the ts_sum over the last 'window' days.
        """
        return df.rolling(window).sum()

    def ts_mean(self, df, window=10):
        """Computes the rolling mean for the given window size.

        Args:
            df (pd.DataFrame): tickers in columns, dates in rows.
            window      (int): size of rolling window.

        Returns:
            pd.DataFrame: the mean over the last 'window' days.
        """
        return df.rolling(window).mean()


    def ts_weighted_mean(self, df, n=10):
        """
        Linear weighted moving average implementation.
        :param df: a pandas DataFrame.
        :param period: the LWMA period
        :return: a pandas DataFrame with the LWMA.
        """
        weights = np.arrange(1, n+1)

        return (df.rolling(n).apply(lambda x:np.dot(x, weights)/weights.sum(), raw=True).to_list())


    def ts_std(self, df, window=10):
        """
        Wrapper function to estimate rolling standard deviation.
        :param df: a pandas DataFrame.
        :param window: the rolling window.
        :return: a pandas DataFrame with the time-series min over the past 'window' days.
        """
        return (df
                .rolling(window)
                .std())

    def ts_rank(self, df, window=10):
        """
        Wrapper function to estimate rolling rank.
        :param df: a pandas DataFrame.
        :param window: the rolling window.
        :return: a pandas DataFrame with the time-series rank over the past window days.
        """
        return (df
                .rolling(window)
                .apply(lambda x: x.rank().iloc[-1]))

    def ts_product(self, df, window=10):
        """
        Wrapper function to estimate rolling ts_product.
        :param df: a pandas DataFrame.
        :param window: the rolling window.
        :return: a pandas DataFrame with the time-series ts_product over the past 'window' days.
        """
        return (df
                .rolling(window)
                .apply(np.prod))

    def ts_max(self, df, window=10):
        """
        Wrapper function to estimate rolling min.
        :param df: a pandas DataFrame.
        :param window: the rolling window.
        :return: a pandas DataFrame with the time-series max over the past 'window' days.
        """
        return df.rolling(window).max()

    def ts_argmax(self, df, window=10):
        """
        Wrapper function to estimate which day ts_max(df, window) occurred on
        :param df: a pandas DataFrame.
        :param window: the rolling window.
        :return: well.. that :)
        """
        return df.rolling(window).apply(np.argmax).add(1)

    def ts_argmin(self, df, window=10):
        """
        Wrapper function to estimate which day ts_min(df, window) occurred on
        :param df: a pandas DataFrame.
        :param window: the rolling window.
        :return: well.. that :)
        """
        return (df.rolling(window)
                .apply(np.argmin)
                .add(1))

    def ts_corr(self, x, y, window=10):
        """
        Wrapper function to estimate rolling correlations.
        :param x, y: pandas DataFrames.
        :param window: the rolling window.
        :return: a pandas DataFrame with the time-series min over the past 'window' days.
        """
        return x.rolling(window).corr(y)

    def ts_cov(self, x, y, window=10):
        """
        Wrapper function to estimate rolling covariance.
        :param df: a pandas DataFrame.
        :param window: the rolling window.
        :return: a pandas DataFrame with the time-series min over the past 'window' days.
        """
        return x.rolling(window).cov(y)
