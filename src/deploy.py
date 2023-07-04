import os, time, json
from utils.uptime import UptimeRobot
from utils.rango import get_sample_routes, get_rango_quote_url, get_rango_swap_url


RANGO_API_KEY = os.environ.get('RANGO_API_KEY')
UPTIME_ROBOT_API_KEY = os.environ.get('UPTIME_ROBOT_API_KEY')

if not RANGO_API_KEY:
    raise Exception("RANGO_API_KEY not found in environment variables")

if not UPTIME_ROBOT_API_KEY:
    raise Exception("UPTIME_ROBOT_API_KEY not found in environment variables")


client = UptimeRobot(api_key=UPTIME_ROBOT_API_KEY)
monitors = client.get_all_monitors()

routes_list = get_sample_routes()['bridges'] + get_sample_routes()['dexes']

for route in routes_list:
    url = get_rango_quote_url(RANGO_API_KEY, route['from'], route['to'], route['amount'], route['swappers'], 3)
    swappers = '-'.join(route['swappers'])
    monitor_url = url
    monitor_name = f'{swappers} Quote'
    keyword_value = "OK"
    interval = "300"

    client.create_or_update_monitor(monitor_name, monitor_url, keyword_value, interval)
    time.sleep(0.5)


for route in routes_list:
    url = get_rango_swap_url(RANGO_API_KEY, route['from'], route['to'], route['amount'], route['swappers'], 3)
    swappers = '-'.join(route['swappers'])
    monitor_url = url
    monitor_name = f'{swappers} Swap'
    from_blockchain = route['from'].split('.')[0]
    keyword_value = "txTo"
    if from_blockchain in ['OSMOSIS', 'COSMOS', 'KUJIRA',  'JUNO']:
        keyword_value = 'signType'
    elif from_blockchain in ['SOLANA']:
        keyword_value = 'txType'
    elif from_blockchain in ['TRON']:
        keyword_value = 'raw_data'
    elif from_blockchain in ['STARKNET']:
        keyword_value = 'calls'

    interval = "300"

    client.create_or_update_monitor(monitor_name, monitor_url, keyword_value, interval)
    time.sleep(0.5)


monitors = client.get_all_monitors()
swappers_monitors_ids = [
    str(monitor['id']) for monitor in monitors 
    if ('Quote' in monitor['friendly_name'] and 'Basic' not in monitor['friendly_name'])
    or ('Swap' in monitor['friendly_name'] and 'Basic' not in monitor['friendly_name'])
]
client.create_or_update_psp('Rango Swappers', swappers_monitors_ids)
