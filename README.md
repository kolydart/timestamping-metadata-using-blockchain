# Timestamping Metadata Using Blockchain

Example code for timestamping any digital document in blockchain. Using web3 package to create transactions on main ethereum network & test network via infura.io node.

Long-term preservation of digital information requires confidence in the credibility and ability of digital archives and systems to consistently provide accessible and usable content. Ensuring that the provided information has remained unchanged over time is a particular challenge. Trusted timestamping is an effective method that allows anyone to prove without any doubt that specific content existed at a particular date and time. A practical approach for trusted timestamping using the Ethereum blockchain is presented here. A complete metadata record is stored as transaction input data along with a document hash digest. The approach is uncomplicated, human and machine readable, self-explanatory, and modular. It supports metadata preservation and copyright protection of digital documents applying verification without disclosure. The approach aims at extending current digital archives and systems using existing, well-tested technology.

Read the full paper:
https://link.springer.com/chapter/10.1007/978-3-030-36599-8_42

## Getting Started

Download repository, update variables and run each python script. The scripts are already populated with metadata from a composer's digital score.

### Prerequisites

* python 3
* shell CLI


### Installing
web3 package is required:
```
pip install web3
pip install json
```


### Quick guide

```
git clone https://github.com/kolydart/timestamping-metadata-using-blockchain.git
cd timestamping-metadata-using-blockchain-master
./testGetElement.py
```

## Deployment

Add additional notes about how to deploy this on a live system

## Using With

* [web3](https://github.com/ethereum/web3.py) - A python interface for interacting with the Ethereum blockchain and ecosystem
* [json] - Python package for handling json

## Author

* **Tassos Kolydas** - (https://www.kolydart.gr/en/)

## License

This project is licensed under the GNU General Public License v3.0 - see the [LICENSE.md](LICENSE.md) file for details
