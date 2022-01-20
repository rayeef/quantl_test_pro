
import json
from pymongo import MongoClient
import cbpro
# import PyMongo and connect to a local, running Mongo instance



if __name__ == "__main__":
    import sys
    import cbpro
    import time


    class MyWebsocketClient(cbpro.WebsocketClient):
        def on_open(self):
            self.url = "wss://ws-feed.pro.coinbase.com/"
            self.products = ["ETH-USD"]
            self.channels = ["ticker"]
            self.message_count = 0
            print("Let's count the messages!")

        def on_message(self, msg):
            print(json.dumps(msg, indent=4, sort_keys=True))
            self.message_count += 1

        def on_close(self):
            print("-- Goodbye! --")


    wsClient = MyWebsocketClient()
    wsClient.start()
    print(wsClient.url, wsClient.products, wsClient.channels)

    ''' need to add Mongo db functionality 
        mongo_client = MongoClient('mongodb://localhost:27017/')
    
        # specify the database and collection
        db = mongo_client.cryptocurrency_database
        BTC_collection = db.BTC_collection
        
        # instantiate a WebsocketClient instance, with a Mongo collection as a parameter
        wsClient = cbpro.WebsocketClient(url="wss://ws-feed.pro.coinbase.com", products="BTC-USD",
            mongo_collection=BTC_collection, should_print=False)
        wsClient.start()
    '''
    try:
        while True:
            print("\nMessageCount =", "%i \n" % wsClient.message_count)
            time.sleep(1)
    except KeyboardInterrupt:
        wsClient.close()

    if wsClient.error:
        sys.exit(1)
    else:
        sys.exit(0)


''' To Do: Real Time orderbook
The OrderBook subscribes to a websocket and keeps a real-time record of the orderbook for the product_id input. 
Please provide your feedback for future improvements.'''

'''
order_book = cbpro.OrderBook(product_id='BTC-USD')
order_book.start()
time.sleep(10)
order_book.close()
'''
