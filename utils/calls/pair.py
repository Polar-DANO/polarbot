from web3 import Web3, HTTPProvider, exceptions

from utils.contracts.getContract import getContract
from utils.config.config import *

class Pair:
    def __init__(self, name):
        self.w3 = Web3(HTTPProvider(provider))
        self.contract = getContract(self.w3, name)

    def getReserves(self):
        return self.contract.functions.getReserves().call()[:2]

    def token0(self):
        return self.contract.functions.token0().call()
