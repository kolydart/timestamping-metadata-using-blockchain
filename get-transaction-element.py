#!/usr/bin/env python

"""Get element from transaction input data using Ethereum network (Sepolia testnet or mainnet)
@see https://web3py.readthedocs.io
Preparation (applies only on first usage):
Create project on infura.io & save api key
"""

from web3 import Web3, HTTPProvider
import json
from dotenv import load_dotenv
import os
import argparse

class GreekEncoder(json.JSONEncoder):
  def default(self, obj):
    if isinstance(obj, str):
      return obj.encode('utf-8').decode('utf-8')
    return super(GreekEncoder, self).default(obj)

# Set up argument parsing
parser = argparse.ArgumentParser(description="Get transaction data from Ethereum network")
parser.add_argument("--network", choices=['testnet', 'mainnet'], default='testnet', help="Choose between testnet (Sepolia) and mainnet (default: testnet)")
parser.add_argument("--hash", help="Transaction hash to retrieve data from")
args = parser.parse_args()

# If no hash is provided, use the default
if args.hash is None:
  if args.network == 'testnet':
      args.hash = '0x7a67ba73634cef953ca1f5ac36ab49490d345815e54966b5d65af4e6bfb75834'
  else:
      args.hash = '0x1181851f70db387c12d75bf17c0a2d20220fbd945d86d961b3c1325d10c63476'

# Load environment variables from .env file
if args.network == 'testnet':
  load_dotenv('.env.testing')
else:
  load_dotenv('.env')

apikey = os.environ.get('API_KEY')
if not apikey:
  raise ValueError("API_KEY not found in env file")

# Set the provider URL based on the chosen network
if args.network == 'testnet':
  provider = f'https://sepolia.infura.io/v3/{apikey}'
  network_name = "Ethereum Sepolia testnet"
else:
  provider = f'https://mainnet.infura.io/v3/{apikey}'
  network_name = "Ethereum mainnet"

w3 = Web3(HTTPProvider(provider))  # connect to blockchain network node

if not w3.is_connected():
  raise Exception(f"Failed to connect to {network_name}")

try:

  transaction = w3.eth.get_transaction(args.hash)  # get transaction

  if transaction is None:
    raise Exception(f"Transaction with hash {args.hash} not found")

  input_data = transaction.input  # get record from transaction input data

  # Convert HexBytes to a regular string, removing '0x' prefix if present
  hex_string = input_data.hex() if isinstance(input_data, bytes) else input_data
  if hex_string.startswith('0x'):
    hex_string = hex_string[2:]

  # Decode hex to UTF-8
  json_data = bytes.fromhex(hex_string).decode('utf-8')
  parsed_data = json.loads(json_data)
  print(f"Parsed JSON data from {network_name}:")
  print(json.dumps(parsed_data, indent=2, ensure_ascii=False, cls=GreekEncoder))

  # Uncomment the following line if you want to print a specific field
  # print(f"kolydas.Hash: {parsed_data['kolydas.Hash']}")

except json.JSONDecodeError as e:
  print(f"Error decoding JSON: {e}")
except KeyError as e:
  print(f"Key not found in JSON data: {e}")
except ValueError as e:
  print(f"Error decoding hex data: {e}")
except Exception as e:
  print(f"An error occurred: {e}")