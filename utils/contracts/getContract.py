from web3.middleware import geth_poa_middleware

from utils.contracts.contractsDatas import datas

def getContract(w3, name):
    w3.middleware_onion.inject(geth_poa_middleware, layer=0)
    addr = w3.toChecksumAddress(datas[name]["address"])
    return w3.eth.contract(address=addr, abi=datas[name]["abi"])
