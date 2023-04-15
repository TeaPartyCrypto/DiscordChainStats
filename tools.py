from web3 import Web3
from requests import get
from os import getenv

node_url = getenv("NODE_URL")


def get_current_supply(node):
    genesis = 4318260000000000000000000
    current_block = node.eth.get_block_number()
    emission = node.to_wei(0.1, 'ether')
    current_supply = node.from_wei(genesis + (current_block * emission), 'ether')
    return current_supply


def get_current_price():
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3',
        'Content-Type': 'application/json',
    }
    url = "https://safe.trade/api/v2/peatio/coinmarketcap/ticker"
    r = get(url, headers=headers)
    if r.status_code == 200:
        data = r.json()["GRAMS_USDT"]
        return data["last_price"], data["quote_volume"]
    return None, None


def get_market_cap():
    node = node_connection()
    supply = get_current_supply(node)
    price = get_current_price()[0]
    if price is None:
        return None
    return float(supply) * float(price)


def get_current_hashrate():
    node = node_connection()
    threshold = 100
    latest_block_number = node.eth.get_block_number()
    latest_block = node.eth.get_block(latest_block_number)
    threshold_block = node.eth.get_block(latest_block_number - threshold)
    block_time = (latest_block["timestamp"] - threshold_block["timestamp"]) / threshold
    difficulty = latest_block["difficulty"]
    hashrate = difficulty / block_time
    return hashrate, block_time


def node_connection():
    node = Web3(Web3.HTTPProvider(node_url))
    return node


def format_hashrate(hashrate):

    if hashrate < 1000:
        return str(round(hashrate, 2)) + " H/s"
    elif hashrate < 1000000:
        return str(round(hashrate / 1000, 2)) + " KH/s"
    elif hashrate < 1000000000:
        return str(round(hashrate / 1000000, 2)) + " MH/s"
    elif hashrate < 1000000000000:
        return str(round(hashrate / 1000000000, 2)) + " GH/s"
    elif hashrate < 1000000000000000:
        return str(round(hashrate / 1000000000000, 2)) + " TH/s"
    elif hashrate < 1000000000000000000:
        return str(round(hashrate / 1000000000000000, 2)) + " PH/s"
    elif hashrate < 1000000000000000000000:
        return str(round(hashrate / 1000000000000000000, 2)) + " EH/s"
    elif hashrate < 1000000000000000000000000:
        return str(round(hashrate / 1000000000000000000000, 2)) + " ZH/s"
    elif hashrate < 1000000000000000000000000000:
        return str(round(hashrate / 1000000000000000000000000, 2)) + " YH/s"
    else:
        return str(round(hashrate, 2)) + " H/s"



if __name__ == "__main__":

    print(get_current_hashrate())
