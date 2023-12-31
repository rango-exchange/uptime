import os, time, json
from utils.uptime import UptimeRobot
from utils.rango import get_sample_routes, get_rango_quote_url, get_rango_swap_url, \
    get_swap_monitoring_keyword_per_blockchain


RANGO_API_KEY = os.environ.get('RANGO_API_KEY')
UPTIME_ROBOT_API_KEY = os.environ.get('UPTIME_ROBOT_API_KEY')
UPTIME_ROBOT_PSP_PASSWORD = os.environ.get('UPTIME_ROBOT_PSP_PASSWORD')
UPTIME_ROBOT_PSP_BASE_URL = os.environ.get('UPTIME_ROBOT_PSP_BASE_URL')

if not RANGO_API_KEY:
    raise Exception("RANGO_API_KEY not found in environment variables")

if not UPTIME_ROBOT_API_KEY:
    raise Exception("UPTIME_ROBOT_API_KEY not found in environment variables")

if not UPTIME_ROBOT_PSP_PASSWORD:
    raise Exception("UPTIME_ROBOT_PSP_PASSWORD not found in environment variables")

if not UPTIME_ROBOT_PSP_BASE_URL:
    raise Exception("UPTIME_ROBOT_PSP_BASE_URL not found in environment variables")


client = UptimeRobot(api_key=UPTIME_ROBOT_API_KEY)

routes_json = get_sample_routes()
dex_routes = [route for route in routes_json['dexes']]
bridges_routes = [route for route in routes_json['bridges']]
routes_list = dex_routes + bridges_routes
bridges = [item['swappers'][0] for item in bridges_routes]
dexes = [item['swappers'][0] for item in dex_routes]

for route in routes_list:
    interval = "300"
    swappers = '-'.join(route['swappers'])
    paused = route.get('paused', False)
    
    # create quote monitor
    monitor_url = get_rango_quote_url(RANGO_API_KEY, route['from'], route['to'], route['amount'], route['swappers'], 3)
    monitor_name = f'{swappers} Quote'
    keyword_value = "OK"
    client.create_or_update_monitor(monitor_name, monitor_url, keyword_value, interval, paused)
    
    # create swap monitor
    monitor_url = get_rango_swap_url(RANGO_API_KEY, route['from'], route['to'], route['amount'], route['swappers'], 3)
    monitor_name = f'{swappers} Swap'
    from_blockchain = route['from'].split('.')[0]
    keyword_value = get_swap_monitoring_keyword_per_blockchain(from_blockchain)
    client.create_or_update_monitor(monitor_name, monitor_url, keyword_value, interval, paused)


# create all psps

monitors = client.get_all_monitors()
password = UPTIME_ROBOT_PSP_PASSWORD

swappers_monitors_ids = client.filter_monitors(monitors, [], True, True)
domain = f'swapper-status.{UPTIME_ROBOT_PSP_BASE_URL}'
client.create_or_update_psp('Rango Swappers', swappers_monitors_ids, domain, 4, password)

swappers_monitors_ids = client.filter_monitors(monitors, bridges, True, True)
domain = f'bridge-status.{UPTIME_ROBOT_PSP_BASE_URL}'
client.create_or_update_psp('Rango Bridges', swappers_monitors_ids, domain, 4, password)

swappers_monitors_ids = client.filter_monitors(monitors, bridges, True, False)
domain = f'bridge-quote-status.{UPTIME_ROBOT_PSP_BASE_URL}'
client.create_or_update_psp('Rango Bridges > Quote', swappers_monitors_ids, domain, 4, password)

swappers_monitors_ids = client.filter_monitors(monitors, bridges, False, True)
domain = f'bridge-swap-status.{UPTIME_ROBOT_PSP_BASE_URL}'
client.create_or_update_psp('Rango Bridges > Swap', swappers_monitors_ids, domain, 4, password)

swappers_monitors_ids = client.filter_monitors(monitors, dexes, True, True)
domain = f'dex-status.{UPTIME_ROBOT_PSP_BASE_URL}'
client.create_or_update_psp('Rango DEXs', swappers_monitors_ids, domain, 4, password)

swappers_monitors_ids = client.filter_monitors(monitors, dexes, True, False)
domain = f'dex-quote-status.{UPTIME_ROBOT_PSP_BASE_URL}'
client.create_or_update_psp('Rango DEXs > Quote', swappers_monitors_ids, domain, 4, password)

swappers_monitors_ids = client.filter_monitors(monitors, dexes, False, True)
domain = f'dex-swap-status.{UPTIME_ROBOT_PSP_BASE_URL}'
client.create_or_update_psp('Rango DEXs > Swap', swappers_monitors_ids, domain, 4, password)
