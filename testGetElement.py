#!/usr/bin/env python

"""Get element from transaction input data using ropsten test ethereum network 
@see https://web3py.readthedocs.io
"""

from web3 import Web3, HTTPProvider
import json

transaction_hash = '0xb3fa48e1609e776d88819d44e3a38365283e4298d6c3479e94b2bd2c379b4bd9'
provider = 'https://ropsten.infura.io'

w3 = Web3(HTTPProvider(provider)) # connect to blockchain network node
transaction = w3.eth.getTransaction(transaction_hash) # get transaction
inputData = transaction.input # get record from transaction input data
json_data = bytearray.fromhex(inputData[2:]).decode() # decode hex to utf-8
print(json.loads(json_data)['dc.Title']) # retrieve record element
print(json.loads(json_data)['kolydas.Hash']) # retrieve record element
