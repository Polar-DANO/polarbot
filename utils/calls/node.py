from web3 import Web3, HTTPProvider, exceptions

from utils.contracts.getContract import getContract
from utils.config.config import *

class Node:
    def __init__(self, name):
        self.w3 = Web3(HTTPProvider(provider))
        self.contract = getContract(self.w3, name)

    def decimals(self):
        return self.contract.functions.decimals().call()

    def getNodePrice(self):
        res = self.contract.functions.getNodePrice().call()
        return res / (10**self.decimals())

    def getClaimTime(self):
        return self.contract.functions.getClaimTime().call()

    def getRewardPerNode(self):
        res = self.contract.functions.getRewardPerNode().call()
        return res / (10**self.decimals())

    def getTotalCreatedNodes(self):
        return self.contract.functions.getTotalCreatedNodes().call()

    def getNodeNumberOf(self, addr):
        addr = self.w3.toChecksumAddress(addr)
        return self.contract.functions.getNodeNumberOf(addr).call()

    def futurUsePool(self):
        return self.contract.functions.futurUsePool().call()
