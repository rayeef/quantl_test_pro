#!/usr/bin/env python
import pandas as pd
import logging
from binance.spot import Spot as Client
from binance.lib.utils import config_logging

config_logging(logging, logging.DEBUG)

spot_client = Client(base_url="https://testnet.binance.vision")
l = ['ETHBUSD','BTCUSDT']
df = pd.DataFrame(columns = ['symbol','bidPrice','bidQty','askPrice','askQty'])
for i in l:
    row = spot_client.book_ticker(i)
    df = df.append(row,ignore_index = True)
print(df)

df = df.set_index('symbol')
