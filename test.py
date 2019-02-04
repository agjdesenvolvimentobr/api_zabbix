import requests
from json import loads
import json
url = 'http://zabbixhomolog.poupex.com.br/api_jsonrpc.php'
headers= {'Content-Type': 'application/json'}
request_object = {
    "jsonrpc": "2.0",
    "method": "user.login",
    "params":{},
    "id": 1,
    "auth": None
}
request_object["params"] =  {"user": "Admin","password": "M0n1t0r1@"} 
json = json.dumps(request_object)
response = requests.post(url, headers=headers , data=json ) 
#response_json = json.loads(response.text)
#y = loads(response.json())
print(response.text)
