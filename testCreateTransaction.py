#!/usr/bin/env python

"""Create transaction on Sepolia test ethereum network
@see https://web3py.readthedocs.io
Preparation (applies only on first usage):
Create new wallet, or use existing
- save wallet address
- save private key (take security measures)
- pour some Sepolia test ether in the wallet (use a Sepolia faucet)
Create project on infura.io
- save api key
- whitelist wallet address
"""

from web3 import Web3, HTTPProvider
from dotenv import load_dotenv
import os
import time

# Load environment variables from .env.testing file
load_dotenv('.env.testing')

address = os.environ.get('WALLET_ADDRESS')
pk = os.environ.get('PRIVATE_KEY')
apikey = os.environ.get('API_KEY')

if not all([address, pk, apikey]):
    raise ValueError("WALLET_ADDRESS, PRIVATE_KEY, or API_KEY not found in .env.testing file")

provider = f'https://sepolia.infura.io/v3/{apikey}'
print(f"Connecting to: https://sepolia.infura.io/v3/{apikey[:6]}...")

# Add a small delay before connecting
time.sleep(1)

w3 = Web3(HTTPProvider(provider))  # connect to blockchain network node

if not w3.is_connected():
    raise Exception("Failed to connect to Ethereum Sepolia network")

print("Successfully connected to the network")

record_utf8 = """
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
"""
record_hex = "0x" + "".join(record_utf8.split()).encode("utf-8").hex()  # convert string to hex & remove all whitespaces

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