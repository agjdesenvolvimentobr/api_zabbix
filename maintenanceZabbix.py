import json
from json import loads
import requests
import datetime

class maintenanceZabbix:
      def __init__(self, user, password):
            self.url = "http://10.10.10.101/zabbix/api_jsonrpc.php"
            self.headers= {"Content-Type": "application/json"}
            self.id = 0
            self.request_object = {"jsonrpc": "2.0","method": "apiinfo.version", "params": {},"auth": None, "id": self.id}
            self.request = None
            self.user = user
            self.password = password
            self.request_object["auth"] = self.conection("user.login")
      #Metodo que fazar conexão do usuario
      def conection(self, method ):
            if method== "user.login":
                  data = self.zabbix_api(method, {"user": self.user,"password":self.password})
                  return data.get("result")
            else:
                  data = self.zabbix_api(method)
                  return data.get("result")
      def get_maintenance(self):
            data = self.zabbix_api("maintenance.get", {"filter":"Aplicação de GMUD Protheus", "limit":1})
            result = data.get("result")
            return result[0].get("maintenanceid") 
      def update_maintenance(self, maintenanceid):
            active_since=int(datetime.datetime.now().timestamp())
            active_till = active_since+600
            timeperiods=[{"start_date":active_since}]
            data = self.zabbix_api("maintenance.update",{"maintenanceid":maintenanceid,"timeperiods":timeperiods})
            print(data)
      #Metodo que fazer requisição no na API do Zabbix
      def zabbix_api(self,method, params= {}):
            try:
                  self.request_object["params"] = params
                  self.request_object["method"] = method
                  self.id=self.id+1
                  self.request = requests.post(self.url, headers=self.headers , json=self.request_object )
                  data = loads(self.request.text)
                  self.request_object["params"] = {}
                  self.request_object["method"] = "apiinfo.version"
                  self.request_object["id"] = self.id 
                  return data
            except BaseException:
                  print("Falha na conexão!")
                  exit()
#Iniciando
if __name__ == '__main__':
      m=maintenanceZabbix("Admin", "zabbix")
      maintenanceid=m.get_maintenance()
      m.update_maintenance(maintenanceid)
