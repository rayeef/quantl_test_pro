from .spot import Spot
from django.http import JsonResponse
import json

class BinanceRest:

    # api_key = '6rQOJtUFhkMGICHob2zFZGPAa4CR0XNE1M2SiCt1Ri6OnpBYTjEKdJjnNDX9RK7n'
    # api_secret = 'QLlaZPkKK7kE8xGkLECSBUPgBG55EWJggAKSBOPisZEtu45DQrn43X3dGzT6F134'

    api_key = ''
    api_secret = ''

    #connect binance
    def connect_binance(request):
        if request.method == 'POST':
            broker_data = json.loads(request.body.decode('utf-8'))['data']
            BinanceRest.api_key = broker_data["key"]
            BinanceRest.api_secret = broker_data["secret"]
            client = Spot(key=BinanceRest.api_key, secret=BinanceRest.api_secret)
            # print("Spot Client connected")
            # print(client.time())
            # Get account information
            account = client.account()
            if (account):
                return JsonResponse({"status": "Success", "data": {"account": json.dumps(account)}})
            else:
                return JsonResponse({"status": "Failure", "message": "Binance Authentication Failed ! Wrong credentials"})


    
    



