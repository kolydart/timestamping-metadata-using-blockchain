#!/usr/bin/env python

"""Create transaction on ropsten test ethereum network
@see https://web3py.readthedocs.io
Preparation (applies only on first usage): 
Create new wallet, or use existing
- save wallet address
- save private key (take security measures)
- pour some rop test ether in the wallet (https://faucet.ropsten.be/)
Create project on infura.io
- save api key
- whitelist wallet address
"""


from web3 import Web3, HTTPProvider

address = 'WALLET_ADDRESS'
pk = "PRIVATE_KEY"
provider = 'https://ropsten.infura.io'
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
record_hex = "0x" + " ".join(record_utf8.split()).encode("utf-8").hex() # convert string to hex & remove double whitespaces

w3 = Web3(HTTPProvider(provider)) # connect to blockchain network node
transaction_content = dict(
    nonce = w3.eth.getTransactionCount(address),
    gasPrice = w3.eth.gasPrice,
    gas = w3.eth.estimateGas({'to': address, 'from': address, 'value': 0, 'data': record_hex}),  # change value at will for a lower fee; too low will result in rejected transaction
    to = address,
    value = 0,
    data=record_hex,
) # prepare transaction content
signed_txn = w3.eth.account.signTransaction(transaction_content, pk) # sign transaction
transaction_hash = w3.eth.sendRawTransaction(signed_txn.rawTransaction) # send transaction 
print(transaction_hash.hex()) # retrieve transaction hash
