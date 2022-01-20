from .authenticated_client import AuthenticatedClient
from django.http import JsonResponse
import json

class Coinbase:

    # key = '82540d74c9f4ec35650e3c2664f8abdc'
    # secret = 'Qspg/xvJzI3r2hcUfU33QFXWwzVV3RXvwMlmM+mYPpHzNxV9zi+kxMMMCZgnkoGMJetkTsKyRk0YF2vWf+TVqw=='
    # passphrase = 'tzjprnhvifj'

    key = ''
    secret = ''
    passphrase = ''

    
    # Connect Coinbase 
    def connect_coinbase(request):
        if request.method == "POST":
            broker_data = json.loads(request.body.decode('utf-8'))['data']
            Coinbase.key = broker_data["key"]
            Coinbase.secret = broker_data["secret"]
            Coinbase.passphrase = broker_data["passphrase"]
            # print(broker_data["key"])
            auth_client = AuthenticatedClient(key=Coinbase.key, b64secret=Coinbase.secret, passphrase=Coinbase.passphrase)
            accounts = auth_client.get_accounts()
            # positions = auth_client.get_position()
            # print(positions)
            if (accounts):
                return JsonResponse({"status": "Success", "data": {"accounts": json.dumps(accounts)}})
            else:
                return JsonResponse({"status": "Failure", "message": "Coinbase Authentication Failed ! Wrong credentials"})
                

    # For testing only
    # print('User Accounts Details')
    # print(accounts)
    # positions = auth_client.get_position()
    # print('User Positions')
    # print(positions)
    # Returns generator:
    # auth_client.get_account_history(key)

    
    # Returns generator:
    # print(auth_client.get_account_holds('a4cb40c1-2aba-49e8-a4eb-807344c387c3'))

    '''
    # Buy 0.01 BTC @ 100 USD
    auth_client.buy(price='100.00',  # USD
                    size='0.01',  # BTC
                    order_type='limit',
                    product_id='BTC-USD')
    '''

    '''
    # Sell 0.01 BTC @ 200 USD
    auth_client.sell(price='200.00',  # USD
                     size='0.01',  # BTC
                     order_type='limit',
                     product_id='BTC-USD')
    '''

    '''
    # Limit order-specific method
    auth_client.place_limit_order(product_id='BTC-USD', 
                              side='buy', 
                              price='200.00', 
                              size='0.01')
    '''

    '''
    # Place a market order by specifying amount of USD to use. 
    # Alternatively, `size` could be used to specify quantity in BTC amount.
    auth_client.place_market_order(product_id='BTC-USD', 
                               side='buy', 
                               funds='100.00')
    '''

    '''
    # Stop order. `funds` can be used instead of `size` here.
    auth_client.place_stop_order(product_id='BTC-USD', 
                              stop_type='loss', 
                              price='200.00', 
                              size='0.01')
    '''

    '''
    #cancel order
    auth_client.cancel_order("d50ec984-77a8-460a-b958-66f114b0de9b")
    '''

    '''
    #cancel all
    auth_client.cancel_all(product_id='BTC-USD')
    '''

    '''
    # Returns generator:
    auth_client.get_orders()
    '''

    '''
    auth_client.get_order("d50ec984-77a8-460a-b958-66f114b0de9b")
    '''

    '''
    # All return generators
    auth_client.get_fills()
    # Get fills for a specific order
    auth_client.get_fills(order_id="d50ec984-77a8-460a-b958-66f114b0de9b")
    # Get fills for a specific product
    auth_client.get_fills(product_id="ETH-BTC")
    '''

    '''
    #deposit & withdraw
    depositParams = {
        'amount': '25.00', # Currency determined by account specified
        'coinbase_account_id': '60680c98bfe96c2601f27e9c'
    }
    auth_client.deposit(depositParams)
    '''

    '''
    # Withdraw from CB Pro into Coinbase Wallet
    withdrawParams = {
            'amount': '1.00', # Currency determined by account specified
            'coinbase_account_id': '536a541fa9393bb3c7000023'
    }
    auth_client.withdraw(withdrawParams)
    '''
