#!/usr/bin/env python

"""Create transaction on Ethereum network (Sepolia testnet or mainnet)
@see https://web3py.readthedocs.io
Preparation (applies only on first usage):
Create new wallet, or use existing
- save wallet address
- save private key (take security measures)
- pour some test ether in the wallet if using testnet (use a Sepolia faucet)
Create project on infura.io
- save api key
- whitelist wallet address
"""

from web3 import Web3, HTTPProvider
from dotenv import load_dotenv
import os
import time
import argparse
import json

# Set up argument parsing
parser = argparse.ArgumentParser(description="Create transaction on Ethereum network")
parser.add_argument("--network", choices=['testnet', 'mainnet'], default='testnet', help="Choose between testnet (Sepolia) and mainnet (default: testnet)")
parser.add_argument("--title", help="dc.Title")
parser.add_argument("--creator", help="dc.Creator")
parser.add_argument("--description", help="dc.Description")
parser.add_argument("--identifier", help="dc.Identifier")
parser.add_argument("--format", help="dc.Format")
parser.add_argument("--rights", help="dc.Rights")
parser.add_argument("--source", help="dc.Source")
parser.add_argument("--hash", help="kolydas.Hash")
parser.add_argument("--hash-type", help="kolydas.Hash.Type")
args = parser.parse_args()

# Load environment variables from .env file
load_dotenv('.env.testing' if args.network == 'testnet' else '.env')

address = os.environ.get('WALLET_ADDRESS')
pk = os.environ.get('PRIVATE_KEY')
apikey = os.environ.get('API_KEY')

if not all([address, pk, apikey]):
    raise ValueError(f"WALLET_ADDRESS, PRIVATE_KEY, or API_KEY not found in .env file")

# Set the provider URL based on the chosen network
if args.network == 'testnet':
    provider = f'https://sepolia.infura.io/v3/{apikey}'
    network_name = "Ethereum Sepolia testnet"
else:
    provider = f'https://mainnet.infura.io/v3/{apikey}'
    network_name = "Ethereum mainnet"

print(f"Connecting to: {network_name}...")

# Add a small delay before connecting
time.sleep(1)

w3 = Web3(HTTPProvider(provider))  # connect to blockchain network node

if not w3.is_connected():
    raise Exception(f"Failed to connect to {network_name}")

print(f"Successfully connected to {network_name}")

# Construct JSON string from provided arguments
record_data = {}
if args.title:
    record_data["dc.Title"] = args.title
if args.creator:
    record_data["dc.Creator"] = args.creator
if args.description:
    record_data["dc.Description"] = args.description
if args.identifier:
    record_data["dc.Identifier"] = args.identifier
if args.format:
    record_data["dc.Format"] = args.format
if args.rights:
    record_data["dc.Rights"] = args.rights
if args.source:
    record_data["dc.Source"] = args.source
if args.hash:
    record_data["kolydas.Hash"] = args.hash
if args.hash_type:
    record_data["kolydas.Hash.Type"] = args.hash_type

# If no arguments were provided, use the default JSON
if not record_data:
    record_data = json.loads("""
    {
      "dc.Title": "Fiction Moments",
      "dc.Creator": "Σφέτσας, Κυριάκος (Sfetsas, Kyriakos)",
      "dc.Description": "Proof of composition",
      "dc.Identifier": "https://www.kolydart.gr/handle/1001",
      "dc.Format": "application/pdf",
      "dc.Rights": "All rights reserved by the author",
      "dc.Source": "https://www.kolydart.gr/download?name=fiction-moments",
      "kolydas.Hash": "52974bec2f5c33209f60acc1cd1f86ccfbefb39b0cba63162d236bc749c7a2622b5b83fc5d5de9e6a9d500374db2bd1434e3338472a16d113ee352786a0b007a",
      "kolydas.Hash.Type": "sha512sum"
    }
    """)

record_utf8 = json.dumps(record_data, ensure_ascii=False, indent=2)
print("JSON Record:")
print(record_utf8)

record_hex = "0x" + record_utf8.encode("utf-8").hex()  # convert string to hex

try:
    transaction_content = {
        'nonce': w3.eth.get_transaction_count(address),
        'gasPrice': w3.eth.gas_price,
        'gas': w3.eth.estimate_gas({'to': address, 'from': address, 'value': 0, 'data': record_hex}),
        'to': address,
        'value': 0,
        'data': record_hex,
    }  # prepare transaction content

    signed_txn = w3.eth.account.sign_transaction(transaction_content, pk)  # sign transaction
    transaction_hash = w3.eth.send_raw_transaction(signed_txn.raw_transaction)  # send transaction
    print(f"Transaction hash: 0x{transaction_hash.hex()}")  # retrieve transaction hash

    # Wait for the transaction to be mined
    transaction_receipt = w3.eth.wait_for_transaction_receipt(transaction_hash)
    print(f"Transaction was mined in block {transaction_receipt['blockNumber']}")

except Exception as e:
    print(f"An error occurred: {e}")