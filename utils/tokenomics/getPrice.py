import requests
import json

def getNativePriceDollar():
    r = requests.get("https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&ids=avalanche-2&page=1")
    return json.loads(r.content)[0]["current_price"]

def getTokenPriceDollar(pair, tokenAddr, otherPrice):
    rsv = pair.getReserves()
    token0Addr = pair.token0()
    relativePrice = rsv[1] / rsv[0] if tokenAddr == token0Addr else rsv[0] / rsv[1]
    return relativePrice * otherPrice

