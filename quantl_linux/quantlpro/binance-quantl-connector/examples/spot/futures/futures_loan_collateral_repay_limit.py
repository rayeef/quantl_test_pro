#!/usr/bin/env python

import logging
from binance.spot import Spot as Client
from binance.lib.utils import config_logging

config_logging(logging, logging.DEBUG)

key = ""
secret = ""

client = Client(key, secret)
logging.info(
    client.futures_loan_collateral_repay_limit(coin="USDT", collateralCoin="BTC")
)
