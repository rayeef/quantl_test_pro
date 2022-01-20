import time
from wscore import WebSocketClient, STOCKS_CLUSTER
import json

''' Polygon Client: Purpose of this file to establish a connection with Polygon server 
    and fetch the real time stock market data via WebSocket connection '''

def connection_message(message):
    print("Connecting to Polygon WebSocket Client", message)
    print(message[39:-2])

"""
def error_handler(ws, error):
    print("Problem with the connection", error)
"""

def close_handler(ws):
    print("WS Connection to Polygon API is now closed")


def main():
    key = "_t__ozhe3p5ACaYlHpPk2y4oEj7KkElP"
    my_client = WebSocketClient(STOCKS_CLUSTER, key, connection_message)
    my_client.run_async()
    f = open("StockList.dat", 'r')
    for line in f:
        jmsg = my_client.subscribe("A."+line)
        print(jmsg)





def on_message(self, msg):
    print(json.dumps(msg, indent=4, sort_keys=True))
    self.message_count += 1

    #my_client.close_connection()


def Trade(stock):

    key = "_t__ozhe3p5ACaYlHpPk2y4oEj7KkElP"
    my_client = WebSocketClient(STOCKS_CLUSTER, key, connection_message)
    my_client.run_async()
    inp = ("T."+stock)
    my_client.subscribe(inp)


def Quote(stock):
    key = "_t__ozhe3p5ACaYlHpPk2y4oEj7KkElP"
    my_client = WebSocketClient(STOCKS_CLUSTER, key, connection_message)
    my_client.run_async()
    inp = ("Q."+stock)
    my_client.subscribe(inp)

"""
def AggregateMinute(stock):
    key = "_t__ozhe3p5ACaYlHpPk2y4oEj7KkElP"
    my_client = WebSocketClient(STOCKS_CLUSTER, key, connection_message)
    my_client.run_async()
    inp = ("AM."+stock)
    my_client.subscribe(inp)
"""

def AggregateSecond(stock):
    key = "_t__ozhe3p5ACaYlHpPk2y4oEj7KkElP"
    my_client = WebSocketClient(STOCKS_CLUSTER, key, connection_message)
    my_client.run_async()
    inp = ("A."+stock)
    my_client.subscribe(inp)


def LIimitUpDown(stock):
    key = "_t__ozhe3p5ACaYlHpPk2y4oEj7KkElP"
    my_client = WebSocketClient(STOCKS_CLUSTER, key, connection_message)
    my_client.run_async()
    inp = ("LULD."+stock)
    my_client.subscribe(inp)


def Imbalance(stock):

    key = "_t__ozhe3p5ACaYlHpPk2y4oEj7KkElP"
    my_client = WebSocketClient(STOCKS_CLUSTER, key, connection_message)
    my_client.run_async()
    inp = ("NOI."+stock)
    my_client.subscribe(inp)

''' Move this part of code outside the client before deployment'''
if __name__ == "__main__":
    main()