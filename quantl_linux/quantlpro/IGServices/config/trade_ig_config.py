#!/usr/bin/env python
# -*- coding:utf-8 -*-
from django.http import JsonResponse
import json


class config(object):

    # username = "shamazkhan86"
    # password = "A330airbus?"
    # api_key = "3dffcba4bd2570d8b36c204ecc92554cc1d11eb4"
    # acc_type = "DEMO"  # LIVE / DEMO
    # acc_number = "KWWGC"

    username = ""
    password = ""
    api_key = ""
    acc_type = "DEMO"  # LIVE / DEMO
    acc_number = ""

    # Connect Broker Credentials Handle
    def connect_broker(request):
        if request.method == "POST":
            print("Connect Broker Credentials")
            # print(json.loads(request.body.decode('utf-8')))
            broker_data = json.loads(request.body.decode('utf-8'))['data']
            print(broker_data["username"])
            config.username = broker_data["username"]
            config.password = broker_data["password"]
            config.api_key = broker_data["apiKey"]
            config.account_type = broker_data["accountType"]

            return JsonResponse({"status": "Success", "message": "Ig Credendials Configured !"})


