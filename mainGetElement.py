#!/usr/bin/env python

"""Get element from transaction input data using main ethereum network via infura.io node
on main ethereum network
@see https://web3py.readthedocs.io
Preparation (applies only on first usage): 
Create project on infura.io & save api key
"""

from web3 import Web3, HTTPProvider
import json

from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

apikey = os.environ.get('API_KEY')
if not apikey:
    raise ValueError("API_KEY not found in .env file")

transaction_hash = '0x1181851f70db387c12d75bf17c0a2d20220fbd945d86d961b3c1325d10c63476'
provider = f'https://mainnet.infura.io/v3/{apikey}'

w3 = Web3(HTTPProvider(provider)) # connect to blockchain network node

if not w3.is_connected():
    raise Exception("Failed to connect to Ethereum network")

try:
    transaction = w3.eth.get_transaction(transaction_hash) # get transaction
except Exception as e:
    print(f"Error retrieving transaction: {e}")
    exit(1)

inputData = transaction.input # get record from transaction input data
# Convert HexBytes to a regular string, removing '0x' prefix if present
hex_string = inputData.hex() if isinstance(inputData, bytes) else inputData
if hex_string.startswith('0x'):
    hex_string = hex_string[2:]

try:
    # Decode hex to UTF-8
    json_data = bytes.fromhex(hex_string).decode('utf-8')
    parsed_data = json.loads(json_data)
    print(parsed_data['dc.Title']) # retrieve record element
    print(parsed_data['kolydas.Hash']) # retrieve record element
except json.JSONDecodeError as e:
    print(f"Error decoding JSON: {e}")
except KeyError as e:
    print(f"Key not found in JSON data: {e}")
except ValueError as e:
    print(f"Error decoding hex data: {e}")