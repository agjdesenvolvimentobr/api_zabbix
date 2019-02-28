import json
from json import loads
import requests
import datetime
import sys

class maintenanceZabbix:
      def __init__(self, user, password,hosts_name,manute_name, time):
            self.url = "http://zabbixhomolog.poupex.com.br/api_jsonrpc.php"
            self.headers= {"Content-Type": "application/json"}
            self.id = 0
            self.request_object = {"jsonrpc": "2.0","method": "apiinfo.version", "params": {},"auth": None, "id": self.id}
            self.request = None
            self.time = time
            self.request_object["auth"] = self.conection("user.login", user, password)
            self.manute_name = manute_name
            self.delete_maintenance(manute_name)
            self.hosts_id = self.get_host(hosts_name)
      #Metodo que fazar conexão do usuario
      def conection(self, method, user, password):
            data = ""
            if method== "user.login":
                  data = self.zabbix_api(method, {"user": user,"password":password})
            else:
                  data = self.zabbix_api(method)
            return data.get("result")
      #Metodo que Obtem manutenção, se existir.
      def delete_maintenance(self,manute_name):
            maintenanceid = 0
            data = self.zabbix_api("maintenance.get", {"output":"maintenanceid","filter":{"name":manute_name}})
            manutes = data.get("result")
            for manute in manutes:
                  maintenanceid = manute.get("maintenanceid")
                  self.zabbix_api("maintenance.delete",[maintenanceid])
            
      #Metodo que busca o ID do host que deve ser usado durante a manutenção
      def get_host(self, hosts_name):
            params={"output": ["hostid"],"filter":{"host": hosts_name}}
            data = self.zabbix_api("host.get",params)
            hosts=data.get("result")
            hosts_id = []
            for host in hosts:
                  hosts_id.append(host.get("hostid"))
            if(len(hosts_id) == 0):
                  print("Hosts informados não foram localizados!")
                  exit(2)
            return hosts_id
      #Metodo que inicia a manutenção
      def start_maintenance(self):
            active_since=int(datetime.datetime.now().timestamp()) - 60
            time=self.time*60
            active_till = active_since+time
            timeperiods=[{"start_date":active_since, "period": time, "timeperiod_type":0}]
            manute_params = {"active_since":active_since,"active_till":active_till,"timeperiods":timeperiods}
            manute_params["name"] = self.manute_name
            manute_params["description"]="Servidor passando por aplicação de GMUD automatica."
            manute_params["hostids"]=self.hosts_id
            self.zabbix_api("maintenance.create", manute_params)         
            print("Manutenção iniciada com sucesso!")
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
                  if(data.get("error")):
                        print(data.get("error"))
                        exit(1) 
                  return data
            except BaseException:
                  print("Falha na conexão!")
                  exit()
#Iniciando
if __name__ == '__main__':
      user=sys.argv[1]
      password=sys.argv[2]
      hosts_name = sys.argv[3].split(',')#nome do host
      manute_name=sys.argv[4]#Titulo da manutenção
      time=15
      if(len(sys.argv) == 6):
            time=int(sys.argv[5])
      manute=maintenanceZabbix(user,password,hosts_name, manute_name,time)
      manute.start_maintenance()