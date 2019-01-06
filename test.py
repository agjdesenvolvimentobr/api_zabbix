"""import requests
from json import loads
import json
url = 'http://10.10.10.101/zabbix/api_jsonrpc.php'
headers= {'Content-Type': 'application/json'}
request_object = {
    "jsonrpc": "2.0",
    "method": "user.login",
    "params":{},
    "id": 1,
    "auth": None
}
request_object["params"] =  {"user": "Admin","password": "zabbix"} 
json = json.dumps(request_object)
response = requests.post(url, headers=headers , data=json ) 
response_json = json.loads(response.text)
y = loads(response.json())
print(y.get("result"))"""
from zabbix.api import ZabbixAPI

# Create ZabbixAPI class instance
zapi = ZabbixAPI(url='http://localhost', user='api', password='zabbix')
print(zapi.do_request('apiinfo.version'))
print(zapi.do_request('user.logout'))

