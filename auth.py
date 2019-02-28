import json
from json import loads
import requests

class UserZabbix:
      def __init__(self, url_zabbix):
            self.url = url_zabbix+"/api_jsonrpc.php"
            self.headers= {"Content-Type": "application/json"}
            self.request_object = {"jsonrpc": "2.0","method": " ", "params": {},"auth": None, "id": 1}
            self.request = None
      def login(self, user, password):
            self.request_object["method"] = "user.login"
            self.request_object["params"] = {"user": user, "password": password}
            try:
                  self.request = requests.post(self.url, headers=self.headers , json=self.request_object )
                  data = loads(self.request.text)
                  return data.get("result")
            except BaseException:
                  print("Falha na conexão!")
                  #print(Response.raise_for_status())
                  return False 
      def logout(self, auth):
            self.request_object["method"] = "user.logout"
            self.request_object["auth"] = auth
            self.request_object["params"] = {}
            print (self.request_object)
            try:
                  self.request = requests.post(self.url, headers=self.headers , json=self.request_object )
                  data = loads(self.request.text)
                  print (data)
                  return data.get("result")
            except BaseException:
                  print("Falha na conexão!")
                  return False
            
      
#print (r.json())
if __name__ == '__main__':
      u=UserZabbix("https://zabbix.poupex.com.br")
      a= u.login("04607528129", "Azaw45402412*")
      print(a)
      out=u.logout(a)
      if out:
            print("Sessão encerrada com sucesso!")
      else:
            print("Falhou!")
