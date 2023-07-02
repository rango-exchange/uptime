import requests, urllib, json, time, os

RANGO_API_KEY = os.environ.get('RANGO_API_KEY')
UPTIME_ROBOT_API_KEY = os.environ.get('UPTIME_ROBOT_API_KEY')

if not RANGO_API_KEY:
    raise Exception("RANGO_API_KEY not found in environment variables")
if not UPTIME_ROBOT_API_KEY:
    raise Exception("UPTIME_ROBOT_API_KEY not found in environment variables")


def get_route(src, dest, amount, swappers, slippage):
    url = "https://api.rango.exchange/basic/quote?"

    params = {
        'from': src,
        'to': dest,
        'amount': amount,
        'swappers': ','.join(swappers),
        'slippage': slippage,
        'apiKey': RANGO_API_KEY
    }

    url += urllib.parse.urlencode(params)
    response = requests.request("GET", url)
    result = response.json()
    resultType = result["resultType"]
    # print(f'{src} => {dest} => {resultType}')
    print(f'{swappers[0]} => {resultType}')
    if resultType != 'OK':
        print(url)
        print(response.text)
        raise Exception(f'Route not found for: {",".join(swappers)}')

routes_list = json.loads(open('src/assets/quotes.json').read())['quotes']

for route in routes_list:
    get_route(route['from'], route['to'], route['amount'], route['swappers'], 3)
    time.sleep(0.5)
    