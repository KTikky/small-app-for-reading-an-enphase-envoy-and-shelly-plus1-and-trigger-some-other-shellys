import json
import requests
user='email@address'
password='password'
envoy_serial='serial_number'
data = {'user[email]': user, 'user[password]': password}
response = requests.post('https://enlighten.enphaseenergy.com/login/login.json?', data=data)
response_data = json.loads(response.text)
data = {'session_id': response_data['session_id'], 'serial_num': envoy_serial, 'username': user}
response = requests.post('https://entrez.enphaseenergy.com/tokens', json=data)
token_raw = response.text
print(token_raw)
