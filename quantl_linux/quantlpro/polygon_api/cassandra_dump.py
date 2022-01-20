from cassandra.cluster import Cluster
from cassandra.auth import PlainTextAuthProvider
import json
import bson
import pandas as pd
from polygon_rest import RESTClient
import datetime

def ts_to_datetime(ts) -> str:
    return datetime.datetime.fromtimestamp(ts / 1000.0).strftime('%Y-%m-%d %H:%M')

cluster = Cluster(['173.201.19.235'], control_connection_timeout=10,  port=9042)
session = cluster.connect()

session.execute('''CREATE KEYSPACE IF NOT EXISTS amd WITH REPLICATION = { 'class' : 'SimpleStrategy', 'replication_factor' : 3 }''')
session.set_keyspace('amd')
#session.execute('CREATE TABLE historical1(Date timestamp,Open float,High float,Low float,Close float,Volume float,PRIMARY KEY (Date))')
query = "INSERT INTO historical1(Date,Open,High,Low,Close,Volume) VALUES (?,?,?,?,?,?)"
prepared = session.prepare(query)

key = "_t__ozhe3p5ACaYlHpPk2y4oEj7KkElP"
# RESTClient can be used as a context manager to facilitate closing the underlying http session
# https://requests.readthedocs.io/en/master/user/advanced/#session-objects
with RESTClient(key) as client:
    from_ = "2000-01-01"
    to = "2022-01-03"

    resp = client.stocks_equities_aggregates('AMD', 1, "day", from_, to, unadjusted=False)
    print(f"Day aggregates for {resp.ticker} between {from_} and {to}.")

    for result in resp.results:
        dt = ts_to_datetime(result["t"])
        jmsg = {"Date": dt,
                "Open": result['o'],
                "High": result['h'],
                "Low": result['l'],
                "Close": result['c'],
                "Volume": result['v']}

        session.execute(prepared,
                        (jmsg['Date'], jmsg['Open'], jmsg['High'], jmsg['Low'], jmsg['Close'], jmsg['Volume']))