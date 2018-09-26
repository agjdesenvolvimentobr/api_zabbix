import json
from json import loads
import requests
import datetime
import sys

class maintenanceZabbix:
      def __init__(self, user, password,host_name,manute_name):
            self.url = "http://10.10.10.101/zabbix/api_jsonrpc.php"
            self.headers= {"Content-Type": "application/json"}
            self.id = 0
            self.request_object = {"jsonrpc": "2.0","method": "apiinfo.version", "params": {},"auth": None, "id": self.id}
            self.request = None
            self.user = user
            self.password = password
            self.request_object["auth"] = self.conection("user.login")
            self.host_name = host_name
            self.manute_name = manute_name
            self.manute = self.get_maintenance()
            self.host_id = self.get_host()
      #Metodo que fazar conexão do usuario
      def conection(self, method ):
            if method== "user.login":
                  data = self.zabbix_api(method, {"user": self.user,"password":self.password})
                  return data.get("result")
            else:
                  data = self.zabbix_api(method)
                  return data.get("result")
      #Metodo que Obtem manutenção, se existir.
      def get_maintenance(self):
            maintenanceid = 0
            data = self.zabbix_api("maintenance.get", {"output":"maintenanceid","filter":{"name":self.manute_name}})
            manutes = data.get("result")
            print(data)
            for manute in manutes:
                  maintenanceid = manute.get("maintenanceid")
            return maintenanceid
      #Metodo que busca o ID do host que deve ser usado durante a manutenção
      def get_host(self):
            params={"output": ["hostid"],"filter":{"host": [self.host_name]}}
            data = self.zabbix_api("host.get",params)
            print(data)
            host=data.get("result")
            return host[0].get("hostid")
      #Metodo que inicia a manutenção
      def start_maintenance(self):
            active_since=int(datetime.datetime.now().timestamp())
            time=1200
            active_till = active_since+time
            timeperiods=[{"start_date":active_since, "period": time, "timeperiod_type":0}]
            manute_params = {"active_since":active_since,"active_till":active_till,"timeperiods":timeperiods}
            data = None
            if self.manute > 0:
                  manute_params["maintenanceid"]= self.manute
                  data = self.zabbix_api("maintenance.update",manute_params)
            else:
                  manute_params["name"] = self.manute_name
                  manute_params["description"]="Servidor passando por aplicação de GMUD automatica."
                  manute_params["hostids"]=[self.host_id]
                  data = self.zabbix_api("maintenance.create", manute_params)
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
      host_name = sys.argv[1]
      manute_name=sys.argv[2]
      manute=maintenanceZabbix("Admin", "zabbix",host_name, manute_name)
      manute.start_maintenance()
     # print(m.get_host("Zabbix server"))
