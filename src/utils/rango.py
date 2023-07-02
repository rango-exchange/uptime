import json, urllib, requests

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

def get_sample_routes():
    routes_list = json.loads(open('src/assets/swappers-quotes.json').read())['quotes']
    return routes_list

def find_route_or_throw_exception(apy_key, src, dest, amount, swappers, slippage):
    url = get_rango_quote_url(apy_key, src, dest, amount, swappers, slippage)
    response = requests.request("GET", url)
    result = response.json()
    result_type = result["resultType"]
    print(f'{swappers[0]} => {result_type}')
    if result_type != 'OK':
        print(f'{swappers}: {src} => {dest} [result = {result_type}]')
        print(response.text)
        raise Exception(f'Route not found for: {swappers}')