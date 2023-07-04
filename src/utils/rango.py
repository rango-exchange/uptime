import json, urllib, requests


def get_sample_routes():
    return json.loads(open('src/assets/sample-quotes.json').read())

def get_sample_accounts():
    return json.loads(open('src/assets/sample-accounts.json').read())

def get_rango_quote_url(api_key, src, dest, amount, swappers, slippage):
    url = "https://api.rango.exchange/basic/quote?"
    swappers = ','.join(swappers)
    params = {
        'from': src,
        'to': dest,
        'amount': amount,
        'swappers': swappers,
        'slippage': slippage,
        'apiKey': api_key
    }

    url += urllib.parse.urlencode(params)
    return url


def get_rango_swap_url(api_key, src, dest, amount, swappers, slippage):
    url = "https://api.rango.exchange/basic/swap?"
    swappers = ','.join(swappers)
    sample_accounts_map = get_sample_accounts()
    src_blockchain = src.split('.')[0]
    dest_blockchain = dest.split('.')[0]
    src_wallet = sample_accounts_map.get(src_blockchain, sample_accounts_map.get("EVM"))
    dest_wallet = sample_accounts_map.get(dest_blockchain, sample_accounts_map.get("EVM"))
    params = {
        'from': src,
        'to': dest,
        'amount': amount,
        'fromAddress': src_wallet,
        'toAddress': dest_wallet,
        'disableEstimate': True,
        'swappers': swappers,
        'slippage': slippage,
        'apiKey': api_key,
    }

    url += urllib.parse.urlencode(params)
    return url

def get_quote_or_throw_exception(apy_key, src, dest, amount, swappers, slippage):
    url = get_rango_quote_url(apy_key, src, dest, amount, swappers, slippage)
    response = requests.request("GET", url)
    result = response.json()
    result_type = result["resultType"]
    print(f'{swappers[0]} => {result_type}')
    if result_type != 'OK':
        print(f'{swappers}: {src} => {dest} [result = {result_type}]')
        raise Exception(f'Route not found for: {swappers}')

def get_swap_or_throw_exception(apy_key, src, dest, amount, swappers, slippage):
    url = get_rango_swap_url(apy_key, src, dest, amount, swappers, slippage)
    response = requests.request("GET", url)
    result = response.json()
    result_type = result["resultType"]
    tx = result["tx"]
    print(f'{swappers[0]} => {result_type}')
    if result_type != 'OK' or not tx:
        print(f'{swappers}: {src} => {dest} [result = {result_type}]')
        raise Exception(f'Swap not found for: {swappers}')

def get_swap_monitoring_keyword_per_blockchain(blockchain):
    if blockchain in ['OSMOSIS', 'COSMOS', 'KUJIRA',  'JUNO']:
        return 'signType'
    elif blockchain in ['SOLANA']:
        return 'txType'
    elif blockchain in ['TRON']:
        return 'raw_data'
    elif blockchain in ['STARKNET']:
        return 'calls'
    else:
        return 'txTo'
