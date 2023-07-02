import requests, urllib, os


RANGO_API_KEY = os.environ.get('RANGO_API_KEY')
UPTIME_ROBOT_API_KEY = os.environ.get('UPTIME_ROBOT_API_KEY')

if not RANGO_API_KEY:
    raise Exception("RANGO_API_KEY not found in environment variables")
if not UPTIME_ROBOT_API_KEY:
    raise Exception("UPTIME_ROBOT_API_KEY not found in environment variables")


url = "https://api.uptimerobot.com/v2/newMonitor"

monitor_url = f'https://api.rango.exchange/basic/quote?from=BSC.USDT--0x55d398326f99059ff775485246999027b3197955&to=POLYGON.USDT--0xc2132d05d31c914a87c6611c10748aeb04b58e8f&amount=100000000000000000000&swappers=Hyphen&apiKey={RANGO_API_KEY}'
monitor_name = "Hyphen Quote 3"
keyword_value = "OK"
interval = "300"

params = {
    'api_key': UPTIME_ROBOT_API_KEY,
    'format': 'json',
    'type': 2,
    'url': monitor_url,
    'friendly_name': monitor_name,
    'keyword_type': 2,
    'keyword_value': keyword_value,
    'interval': interval
}

payload = urllib.parse.urlencode(params)
headers = {
    'cache-control': "no-cache",
    'content-type': "application/x-www-form-urlencoded"
    }
          
response = requests.request("POST", url, data=payload, headers=headers)
          
print(response.text)
