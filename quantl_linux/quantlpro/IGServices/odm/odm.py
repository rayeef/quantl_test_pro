# -*- coding: utf-8 -*-
"""
Created on Mon Aug 30 16:29:23 2021
Author: Shamaz Khan
Organisation: Quantl AI Ltd
"""
import json
import logging
import bson
from bson import json_util
from rest import IGService
from stream import IGStreamService
from lightstreamer import Subscription
from pymongo import MongoClient
from datetime import datetime

from bson import Binary, Code
from bson.json_util import dumps

def wait_for_input():
    input("{0:-^80}\n".format("HIT CR TO UNSUBSCRIBE AND DISCONNECT FROM \
                                      LIGHTSTREAMER"))

class config(object):
    username = "shamazkhan86"
    password = "A330airbus?"
    api_key = "3dffcba4bd2570d8b36c204ecc92554cc1d11eb4"
    acc_type = "DEMO"  # LIVE / DEMO
    acc_id = "Z3TMKL"


logging.basicConfig(level=logging.INFO)
# logging.basicConfig(level=logging.DEBUG)

ig_service = IGService(
    config.username, config.password, config.api_key, config.acc_type, acc_id=config.acc_id
)

ig_stream_service = IGStreamService(ig_service)
ig_stream_service.create_session()
dlist = ['CHART:CS.D.GBPUSD.CFD.IP:SECOND',
         'CHART:CS.D.USDJPY.CFD.IP:SECOND',
         'CHART:CS.D.AUDUSD.CFD.IP:SECOND']



''' JSON serialization & formatting for MongoDB'''
def on_item_update(item_update):
    # print("price: %s " % item_update)

    now = datetime.now()
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
    jmsg = {'Date': dt_string, 'ID': ('{stock_name:<19}'.format(
        stock_name=item_update["name"], **item_update["values"])),
            'Bid Open': float ("{BID_OPEN:>5}".format(
                stock_name=item_update["name"], **item_update["values"])),
            'Bid high': float ('{BID_HIGH:>5}'.format(
                stock_name=item_update["name"], **item_update["values"])),
            'Bid low': float ('{BID_LOW:>5}'.format(
                stock_name=item_update["name"], **item_update["values"])),
            'Bid close': float ('{BID_CLOSE:>5}'.format(
                stock_name=item_update["name"], **item_update["values"]))
            }
    '''BSON Verification  - expected output must be binary'''
    bmsg = bson.BSON.encode(jmsg)
    #print(bmsg)
    print(jmsg)

def ig_dump():
    for i in dlist:
        subscription = Subscription(
            mode="MERGE",
            items=[i], # sample CFD epics
            #items=["L1:CS.D.GB'PUSD.TODAY.IP", "L1:IX.D.FTSE.DAILY.IP"], # sample spreadbet epics
            fields=['BID_OPEN','BID_HIGH','BID_LOW','BID_CLOSE'],
        )
        '''Subscriber settings & end calls'''
        subscription.addlistener(on_item_update)
        sub_key = ig_stream_service.ls_client.subscribe(subscription)

'''kick start dumping process'''
ig_dump()
wait_for_input()
# Unsubscribing from Lightstreamer by using the subscription key
# Disconnecting
ig_stream_service.disconnect()
