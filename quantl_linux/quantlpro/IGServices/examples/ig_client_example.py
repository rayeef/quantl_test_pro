# -*- coding: utf-8 -*-
"""
Created on Wed Aug 25 14:19:32 2021
Author: Shamaz Khan
Organisation: Quantl AI Ltd
"""


from IGServices.rest import IGService

# Required User details
userName = 'ShamazKhan'
secureWord = 'A330airbus'
APIKey = 'd8253bf4a2eece83585a8e317360e430173d050a'

#Establish Connection to IG Trade
ig_trade = IGService(userName,
                       secureWord,
                       APIKey)
currentSession = ig_trade.create_session()
print(currentSession)
print('Account owned by user', userName)
userAccounts = ig_trade.fetch_accounts()
print(userAccounts)
