import requests, urllib


class UptimeRobot:
    def __init__(self, api_key):
        self.api_key = api_key

    def get_all_monitors(self):
        result = []
        offset = 0
        while True:
            url = "https://api.uptimerobot.com/v2/getMonitors"
            payload = f"api_key={self.api_key}&format=json&logs=1&offset={offset}"
            headers = {
                'content-type': "application/x-www-form-urlencoded",
                'cache-control': "no-cache"
            }
            response = requests.request("POST", url, data=payload, headers=headers)
            monitors = response.json()
            result += monitors['monitors']
            offset += 50
            if (len(monitors['monitors']) < 50):
                break
        return result

    def get_monitor_id(self, all_monitors, monitor_name):
        for monitor in all_monitors:
            if monitor['friendly_name'] == monitor_name:
                return monitor['id']
        return None

    def create_monitor(self, name, url, keyword, interval):
        base_url = "https://api.uptimerobot.com/v2/newMonitor"
        params = {
            'api_key': self.api_key,
            'format': 'json',
            'friendly_name': name,
            'url': url,
            'type': 2,
            'keyword_type': 2,
            'keyword_value': keyword,
            'interval': interval
        }
        payload = urllib.parse.urlencode(params)
        headers = {
            'cache-control': "no-cache",
            'content-type': "application/x-www-form-urlencoded"
        }
        response = requests.request("POST", base_url, data=payload, headers=headers)
        print(f'status: {response.status_code}')

    def edit_monitor(self, id, name, url, keyword, interval):
        base_url = "https://api.uptimerobot.com/v2/editMonitor"
        params = {
            'api_key': self.api_key,
            'format': 'json',
            'id': id,
            'friendly_name': name,
            'url': url,
            'type': 2,
            'keyword_type': 2,
            'keyword_value': keyword,
            'interval': interval
        }
        payload = urllib.parse.urlencode(params)
        headers = {
            'cache-control': "no-cache",
            'content-type': "application/x-www-form-urlencoded"
        }
        response = requests.request("POST", base_url, data=payload, headers=headers)
        print(f'status: {response.status_code}')

    def create_or_update_monitor(self, name, url, keyword, interval):
        all_monitors = self.get_all_monitors()
        monitor_id = self.get_monitor_id(all_monitors, name)
        if monitor_id:
            print(f"Found monitor id: {monitor_id} for {name}, editing monitor ...")
            self.edit_monitor(monitor_id, name, url, keyword, interval)
        else:
            print(f"No monitor found for {name}, creating new monitor ...")
            self.create_monitor(name, url, keyword, interval)

    def delete_monitor(self, id):
        url = "https://api.uptimerobot.com/v2/deleteMonitor"
        payload = f"api_key={self.api_key}&format=json&id={id}"
        headers = {
            'cache-control': "no-cache",
            'content-type': "application/x-www-form-urlencoded"
        }
        response = requests.request("POST", url, data=payload, headers=headers)
        print(f'status: {response.status_code}')

    def get_all_psps(self):
        url = "https://api.uptimerobot.com/v2/getPSPs"
        payload = f"api_key={self.api_key}&format=json"
        headers = {
            'content-type': "application/x-www-form-urlencoded",
            'cache-control': "no-cache"
        }
        response = requests.request("POST", url, data=payload, headers=headers)
        psps = response.json()['psps']
        print(f'Found {len(psps)} psps')
        return psps

    def get_psp_id(self, all_psps, psp_name):
        for psp in all_psps:
            if psp['friendly_name'] == psp_name:
                return psp['id']
        return None
    
    def create_psp(self, name, monitors_ids):
        url = "https://api.uptimerobot.com/v2/newPSP"
        params = {
            'api_key': self.api_key,
            'format': 'json',
            'type': 1,
            'friendly_name': name,
            'monitors': '-'.join(monitors_ids),
            'hide_url_links': True
        }
        payload = urllib.parse.urlencode(params)
        headers = {
            'cache-control': "no-cache",
            'content-type': "application/x-www-form-urlencoded"
        }
        response = requests.request("POST", url, data=payload, headers=headers)
        print(f'status: {response.status_code}')

    def edit_psp(self, id, name, monitors_ids):
        url = "https://api.uptimerobot.com/v2/editPSP"
        params = {
            'api_key': self.api_key,
            'format': 'json',
            'type': 1,
            'id': id,
            'friendly_name': name,
            'monitors': '-'.join(monitors_ids),
            'hide_url_links': True
        }
        payload = urllib.parse.urlencode(params)
        headers = {
            'cache-control': "no-cache",
            'content-type': "application/x-www-form-urlencoded"
        }
        response = requests.request("POST", url, data=payload, headers=headers)
        print(f'status: {response.status_code}')

    def create_or_update_psp(self, name, monitors_ids):
        all_psps = self.get_all_psps()
        psp_id = self.get_psp_id(all_psps, name)
        if psp_id:
            print(f"Found psp id: {psp_id} for {name}, editing psp ...")
            self.edit_psp(psp_id, name, monitors_ids)
        else:
            print(f"No psp found for {name}, creating new psp ...")
            self.create_psp(name, monitors_ids)
