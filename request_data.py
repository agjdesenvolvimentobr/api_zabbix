import json
from json import loads
import requests    
  
      
      class Request_api:
            def __init__(method, params = {}, auth = None):
                  self.url = "http://10.10.10.101/zabbix/api_jsonrpc.php"
                  self.headers= {"Content-Type": "application/json"}
                  self.request_object = {"jsonrpc": "2.0","method": method, "params": params,"auth": auth, "id": 1}
                  self.request = None
            try:
                  self.request = requests.post(self.url, headers=self.headers , json=self.request_object )
                  data = loads(self.request.text)
                  return data
            except BaseException:
                  print("Falha na conexão!")
                  return None 