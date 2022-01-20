from IGServices.config.trade_ig_config import *
from IGServices.config import *
from IGServices.rest import IGService
import logging
import requests

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
# if you need to cache to DB your requests
from datetime import timedelta
import requests_cache

def ig_fetch_accounts():
    logging.basicConfig(level=logging.DEBUG)

    expire_after = timedelta(hours=1)
    session = requests_cache.CachedSession(
        cache_name="cache", backend="sqlite", expire_after=expire_after
    )
    # set expire_after=None if you don't want cache expiration
    # set expire_after=0 if you don't want to cache queries

    # config = IGServiceConfig()

    # no cache
    ig_service = IGService(
        config.username, config.password, config.api_key, config.acc_type, acc_id=config.acc_number
    )

    # if you want to globally cache queries
    # ig_service = IGService(config.username, config.password, config.api_key, config.acc_type, session)

    ig_service.create_session()
    # ig_stream_service.create_session(version='3')

    accounts = ig_service.fetch_accounts()

    OpenPositions = ig_service.fetch_open_positions()


    Name = []
    Size = []
    Direction = []
    Value = []
    for i in range(len(OpenPositions)):
        a = OpenPositions.loc[i, 'market']
        Name.append(a['instrumentName'])
        b = OpenPositions.loc[i, 'position']
        Size.append(b['dealSize'])
        Direction.append(b['direction'])
        val = b['dealSize'] * b['openLevel']
        Value.append(val)

    position = OpenPositions.loc[0,'market']
    Name = position['instrumentName']
    print(Name)


    account_1 = accounts.loc[0, 'accountName']
    balance1 = accounts.loc[0, 'balance']
    account_1_balance = balance1['balance']
    pl1 = balance1['profitLoss']

    account_2 = accounts.loc[1, 'accountName']
    balance2 = accounts.loc[1, 'balance']
    account_2_balance = balance2['balance']
    pl2 = balance2['profitLoss']



    return account_1, account_1_balance, pl1, \
           account_2, account_2_balance, pl2, Name, Size, Direction, Value


# df = ig_fetch_accounts()
# print(df)
