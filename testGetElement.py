#!/usr/bin/env python

"""Get element from transaction input data using Sepolia test ethereum network
@see https://web3py.readthedocs.io
"""

from web3 import Web3, HTTPProvider
import json
from dotenv import load_dotenv
import os

class GreekEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, str):
            return obj.encode('utf-8').decode('utf-8')
        return super(GreekEncoder, self).default(obj)

# Load environment variables from .env file
load_dotenv('.env.testing')

apikey = os.environ.get('API_KEY')
if not apikey:
    raise ValueError("API_KEY not found in .env.testing file")

# This is a sample transaction hash from Sepolia. You'll need to replace it with a valid one.
transaction_hash = '0x962e3baa09fb0ed307aad4085f90b21f4c54826781b72763193af6a84981278b'
provider = f'https://sepolia.infura.io/v3/{apikey}'

w3 = Web3(HTTPProvider(provider))  # connect to blockchain network node

if not w3.is_connected():
    raise Exception("Failed to connect to Ethereum Sepolia network")

try:
    transaction = w3.eth.get_transaction(transaction_hash)  # get transaction

    if transaction is None:
        raise Exception(f"Transaction with hash {transaction_hash} not found")

    input_data = transaction.input  # get record from transaction input data

    # Convert HexBytes to a regular string, removing '0x' prefix if present
    hex_string = input_data.hex() if isinstance(input_data, bytes) else input_data
    if hex_string.startswith('0x'):
        hex_string = hex_string[2:]

    # Decode hex to UTF-8
    json_data = bytes.fromhex(hex_string).decode('utf-8')
    parsed_data = json.loads(json_data)
    print("Parsed JSON data:")
    print(json.dumps(parsed_data, indent=2, ensure_ascii=False, cls=GreekEncoder))  # Print formatted JSON with Greek characters

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