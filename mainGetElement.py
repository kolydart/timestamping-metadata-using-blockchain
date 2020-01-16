#!/usr/bin/env python

"""Get element from transaction input data using main ethereum network via infura.io node
on main ethereum network
@see https://web3py.readthedocs.io
Preparation (applies only on first usage): 
Create project on infura.io & save api key
"""

from web3 import Web3, HTTPProvider
import json

apikey = 'API_KEY'
transaction_hash = '0x1181851f70db387c12d75bf17c0a2d20220fbd945d86d961b3c1325d10c63476'
provider = 'https://mainnet.infura.io/v3/'+apikey

w3 = Web3(HTTPProvider(provider)) # connect to blockchain network node
transaction = w3.eth.getTransaction(transaction_hash) # get transaction
inputData = transaction.input # get record from transaction input data
json_data = bytearray.fromhex(inputData[2:]).decode() # decode hex to utf-8
print(json.loads(json_data)['dc.Title']) # retrieve record element
print(json.loads(json_data)['kolydas.Hash']) # retrieve record element

