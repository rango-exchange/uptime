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
# monitors = client.get_all_monitors()
# swappers_monitors_ids = [
#     str(monitor['id']) for monitor in monitors 
#     if ('Quote' in monitor['friendly_name'] and 'Basic' not in monitor['friendly_name'])
#     or ('Swap' in monitor['friendly_name'] and 'Basic' not in monitor['friendly_name'])
# ]
# for monitor in swappers_monitors_ids:
#     client.delete_monitor(monitor)

# psps = client.get_all_psps()
# psps_monitors_ids = [
#     str(psp['id']) for psp in psps 
#     if (psp['friendly_name'] not in ['Rango Status', 'Rango Internal Status'])
# ]
# for psp_id in psps_monitors_ids:
#     client.delete_psp(psp_id)