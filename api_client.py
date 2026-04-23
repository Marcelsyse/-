import json
import requests

def get_rate(from_cur, to_cur):
    with open('config.json', 'r') as f:
        config = json.load(f)
    url = f"https://v6.exchangerate-api.com/v6/{config['api_key']}/pair/{from_cur}/{to_cur}"
    response = requests.get(url)
    data = response.json()
    if data['result'] == 'success':
        return data['conversion_rate']
    else:
        raise Exception('API error')
