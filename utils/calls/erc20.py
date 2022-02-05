from web3 import Web3, HTTPProvider, exceptions

from utils.contracts.getContract import getContract
from utils.config.config import *

class Erc20:
    def __init__(self, name):
        self.w3 = Web3(HTTPProvider(provider))
        self.contract = getContract(self.w3, name)

    def totalSupply(self):
        res = self.contract.functions.totalSupply().call()
        return int(res / (10**self.decimals()))

    def decimals(self):
        return self.contract.functions.decimals().call()

    def name(self):
        return self.contract.functions.name().call()

    def symbol(self):
        return self.contract.functions.symbol().call()

    def balanceOf(self, addr):
        addr = self.w3.toChecksumAddress(addr)
        res = self.contract.functions.balanceOf(addr).call()
        return res / (10**self.decimals())
