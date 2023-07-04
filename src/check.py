import requests, urllib, json, time, os
from utils.rango import get_rango_quote_url, get_sample_routes, \
    get_quote_or_throw_exception


RANGO_API_KEY = os.environ.get('RANGO_API_KEY')
UPTIME_ROBOT_API_KEY = os.environ.get('UPTIME_ROBOT_API_KEY')

if not RANGO_API_KEY:
    raise Exception("RANGO_API_KEY not found in environment variables")
if not UPTIME_ROBOT_API_KEY:
    raise Exception("UPTIME_ROBOT_API_KEY not found in environment variables")

routes = get_sample_routes()
dex_routes = routes['dexes']
bridges_routes = routes['bridges']
routes_list = dex_routes + bridges_routes

for route in routes_list:
    get_quote_or_throw_exception(
        RANGO_API_KEY,
        route['from'], 
        route['to'], 
        route['amount'], 
        route['swappers'], 
        3
    )
    # time.sleep(0.5)
