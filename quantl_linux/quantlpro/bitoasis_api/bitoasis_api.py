import requests
from django.http import JsonResponse
import json

# auth_key = 'fb7e2780-8e09-4cf4-91b1-e3766180498c'


class BearerAuth(requests.auth.AuthBase):
    def __init__(self, token):
        self.token = token

    def __call__(self, r):
        r.headers["authorization"] = "Bearer " + self.token
        return r


'''------------------------ACCOUNTS & BALANCES----------------------------------------------------------------------'''


def get_balances_list():
    """
    Returns a list of accounts that have a balance.
    RESPONSE SCHEMA:
    ----------------

    object:  Returns currency as key and amount as value.
    """
    url = 'https://api.bitoasis.net/v1/exchange/balances'
    result = requests.get(url, auth=BearerAuth(auth_key))
    return result


def deposit_history(ticker):
    """
    Returns a list of digital currency deposits. The list is ordered by data_created in descendant order.

    RESPONSE SCHEMA: application/json
    id: integer
        Order identifier

    amount:	object
            tx_hash
            string or null (Transaction hash)
            could be null when deposit is created between 2 different exchange wallets

    date_created:string <date> (Deposit order creation date)

    status: string
            Enum: "UNCONFIRMED" "PENDING" "DONE" "CANCELED"

    deposit_address: string or null (Deposit address)
                     could be null only in some negligible cases (system does not have the address, very old deposits)

    parsed_deposit_address: object
    """
    url = 'https://api.bitoasis.net/v1/exchange/coin-deposits/' + ticker
    result = requests.get(url, auth=BearerAuth(auth_key))
    return result


def new_coin_deposit(ticker):
    """
    Success response. Returns the digital currency deposit address.

    RESPONSE SCHEMA:
    ---------------
    address: string
            parsed_address
            object (parsed_address)
            in case of additional information included in address (e.g. XRP tag or XLM Memo)
            this item provides parsed address
    """
    url = 'https://api.bitoasis.net/v1/exchange/coin-deposit'
    params = {
        "ticker": ticker
    }
    result = requests.post(url, params=params, auth=BearerAuth(auth_key))
    return result


def fiat_deposit_list():
    """
    Success Response. Returns the history of fiat deposits
    RESPONSE SCHEMA:
    ----------------
    status: string (status7)
            Enum: "UNCONFIRMED" "PENDING" "DONE" "CANCELED" "PROCESSING"
    type:	string (type)
            Enum: "DEPOSIT_BY_WIRE" "DEPOSIT_BY_KNET" "CASH_DEPOSIT"
    """

    url = 'https://api.bitoasis.net/v1/exchange/fiat-deposits'
    result = requests.post(url, auth=BearerAuth(auth_key))
    return result


'''-------------------WITHDRAWLS---------------------------------------------------------------------------------'''


def withdraw_coin(currency, amount, withdrawl_address, withdrawl_address_id):
    """
    Success Response. Creates a digital currency withdrawal. Please note that we have added withdrawal confirmation
    via e-mail and SMS/TOTP as a basic layer of protectection.

    REQUEST BODY SCHEMA: application/json
    currency: required string
              crypto currency symbol - supported values

    amount: required number
            format it as string (for compatibility of currencies with long decimal part, e.g. ETH)

    withdrawal_address: string

    withdrawal_address_id: string
                           additional address identifier (e.g. XRP tag or XLM memo)



    RESPONSE SCHEMA:
    ------------------
    tx_hash	: string or null
            could be null when external withdrawal is created

    status: string (status4)
             Enum: "PROCESSING" "PENDING" "DONE" "CANCELED"

    withdrawal_address:	parsed_withdrawal_address
                        object (parsed_withdrawal_address)
                         in case additional information is included in the address (e.g. XRP tag or XLM memo),
                         this item provides parsed withdrawal_address
    """

    url = 'https://api.bitoasis.net/v1/exchange/coin-withdrawal'
    params = {
        "currency": currency,
        "amount": amount,
        "withdrawl_address": withdrawl_address,
        "withdrawl_address_id": withdrawl_address_id
    }

    result = requests.post(url, params=params, auth=BearerAuth(auth_key))
    return result


def get_withdrawl_fee():
    url = 'https://api.bitoasis.net/v1/exchange/coin-withdrawal-fees'
    result = requests.get(url, auth=BearerAuth(auth_key))
    return result


'''-------------------MARKET DATA -------------------------------------------------------------------------------'''


def get_ticker_data(ticker):
    '''
    TICKER
    RESPONSE SCHEMA:
    ----------------

    ticker: required object (Ticker)
    '''

    url = 'https://api.bitoasis.net/v1/exchange/ticker/' + ticker
    result = requests.get(url, auth=BearerAuth(auth_key))
    return result


def order_book(ticker):
    """
    Success Response. Returns the orderbook of a specific pair.
    Bids are ordered by price in descendant order.
    Asks are ordered by price in ascendant order.

    RESPONSE SCHEMA:
    ----------------

    pair: required string
    bids: required Array of objects (Bid)
    asks: required Array of objects (Ask)

    """

    url = 'https://api.bitoasis.net/v1/exchange/order-book/' + ticker
    result = requests.get(url, auth=BearerAuth(auth_key))
    return result


def get_trades(ticker, key):
    """
    Success Response. Returns the overall trade history of a specific pair

    RESPONSE SCHEMA:
    ----------------

    type: string (type5)
          Enum: "buy" "sell"
    """
    url = 'https://api.bitoasis.net/v1/exchange/trades/' + ticker
    result = requests.get(url, auth=BearerAuth(key))
    return result


'''-------------------ORDER EXECUTION & MANAGEMENT-------------------------------------------------------------'''


def order_list(pair):
    """Success response. Returns the history of Pro exchange orders for a specific pair.

    REQUEST PARAMETER
    -----------------

    pair: string
          currency pair (crypto-fiat, crypto-crypto) - supported values

    QUERY SCHEMA
    ---------------

    offset: integer

    limit: 	integer
            maximal value is 1000

    from_date: string <date>

    status: string one of OPEN, DONE, CANCELED

    RESPONSE SCHEMA
    ---------------
    status	:string (status11)
            Enum: "OPEN" "DONE" "CANCELED" "UNCONFIRMED"
             Order can get to UNCONFIRMED status only in rare cases. It will get resolved to OPEN or CANCELED
             after a short period of time.

    price: 	number or null
            null for market order, limit price for limit order

    avg_execution_price:  number or null
                        null when in OPEN status (or CANCELED before execution),
                        number in string format otherwise

    fee: number
        decimal value of percentage fee formatted as string (e.g. 0.4% fee => 0.004 decimal fee)
    """
    url = 'https://api.bitoasis.net/v1/exchange/orders/' + pair
    params = {
        "pair": pair,

    }
    result = requests.get(url, params=params, auth=BearerAuth(auth_key))
    return result


def order_detail(id):
    '''
    RESPONSE SCHEMA
    ---------------

    status: string (status11)
            Enum: "OPEN" "DONE" "CANCELED" "UNCONFIRMED"
            Order can get to UNCONFIRMED status only in rare cases.
            It will get resolved to OPEN or CANCELED after a short period of time.

    price: 	string or null
            null for market order, limit price for limit order

    avg_execution_price: number or null
                        null when in OPEN status, number in string format otherwise

    fee: number
         decimal value of percentage fee formatted as string (e.g. 0.4% fee => 0.004 decimal fee)
    '''

    url = 'https://api.bitoasis.net/v1/exchange/order/' + id
    params = {
        "id": id
    }

    result = requests.get(url, params=params, auth=BearerAuth(auth_key))
    return result


def order(side, type, pair, amount, price):
    '''
    REQUEST SCHEMA
    --------------

    side: (required) string (side) Enum: "buy" "sell"

    type: (required) string (type4) Enum: "limit" "market" "stop" "stop_limit"

    pair: (required) string currency pair (crypto-fiat, crypto-crypto)

    amount: (required) number format it as string (for compatibility of currencies with long decimal part, e.g. ETH)

    price: 	number limit price, required within limit type

    stop_price:  number stop price, required within stop and stop limit type

    RESPONSE SCHEMA
    ---------------

    status: string (status11) Enum: "OPEN" "DONE" "CANCELED" "UNCONFIRMED"
            Order can get to UNCONFIRMED status only in rare cases.
            It will get resolved to OPEN or CANCELED after a short period of time.

    price: number or null - null for market order, limit price for limit order

    avg_execution_price:  number or null - null when in OPEN status, number in string format otherwise

    fee: number decimal value of percentage fee formatted as string (e.g. 0.4% fee => 0.004 decimal fee)

    stop_price: number available only for stop and stop limit type

    date_stop_price_triggered: 	string or null
                                available only for stop and stop limit type,
                                null if stop price hasn't been triggered yet
    '''

    url = 'https://api.bitoasis.net/v1/exchange/order'
    params = {
        "side": side,
        "type": type,
        "pair": pair,
        "amount": amount,
        "price": price
    }

    result = requests.post(url, params=params, auth=BearerAuth(auth_key))
    return result


def cancel_order(id):
    '''
    Order cancelling might not be instant. Order could be still OPEN status for a while before switch to CANCEL state
    (it takes few seconds to get cancel status)

    RESPONSE SCHEMA:
    ----------------
    is_canceled: boolean

    Status: string (status11)
            Enum: "OPEN" "DONE" "CANCELED" "UNCONFIRMED"
            Order can get to UNCONFIRMED status only in rare cases.
            It will get resolved to OPEN or CANCELED after a short period of time.

    price: number or null null for market order, limit price for limit order

    avg_execution_price: number or null null when in OPEN status, number in string format otherwise

    fee: number decimal value of percentage fee formatted as string (e.g. 0.4% fee => 0.004 decimal fee)
    '''

    url = 'https://api.bitoasis.net/v1/exchange/cancel-order'
    params = {
        "id": id
    }

    result = requests.post(url, params=params, auth=BearerAuth(auth_key))
    return result


'''
def order():
    url = 'https://api.bitoasis.net/v1/exchange/order'
    params = {
        "side": "buy",
        "type": "limit",
        "pair": "BTC-AED",
        "amount": "10.0",
        "price": "900.0"
        }

    result = requests.post(url, params=params, auth=BearerAuth(auth_key))
    return result
'''

'''For testing only - code below this line is not for production'''
# a = order("buy","limit","BTC-AED","10.0","900.0")  example for order
# a = get_trades("BTC-AED")
# jmsg = json.loads(a.text)
# print(jmsg)

def connect_bitoasis(request):
    if request.method == "POST":
        broker_data = json.loads(request.body.decode('utf-8'))['data']
        key= broker_data["key"]
        print("key ->",key)
        # auth_client = BearerAuth(key)
        check_trades = get_trades("BTC-AED", key)
        print("Checking trades ->", check_trades)
        if (check_trades):
            return JsonResponse({"status": "Success", "data": {"checkTrades": json.dumps(check_trades.text)}})
        else:
            return JsonResponse({"status": "Failure", "message": "Bitoasis Authentication Failed ! Wrong credentials"})

