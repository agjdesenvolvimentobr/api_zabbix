import json
import urllib3
from json import loads
import requests
import sys
import csv

class AddUser():

    def __init__(self):
        self.url = "https://zabbix.poupex.com.br"
        self.user ="04607528129"
        self.password = "Azaw45402412*"
        self.id = 0
        self.headers= {"Content-Type": "application/json"}
        self.request_object = {"jsonrpc": "2.0","method": "apiinfo.version", "params": {},"auth": None, "id": self.id}
        self.request_object["auth"] = self.conection("user.login")

    def conection(self, method ):
            if method== "user.login":
                  data = self.zabbix_api(method, {"user": self.user,"password":self.password})
                  return data.get("result")
            else:
                  data = self.zabbix_api(method)
                  return data.get("result")
    def add_multiplos_users(self):
        nome_ficheiro = 'D:/Amilson/workspace/python/api_zabbix/empregados_codti.csv'
        method="user.create"
        with open(nome_ficheiro, 'r',encoding="utf8") as ficheiro:
            reader = csv.reader(ficheiro, delimiter=',', )
            try:
                for [index,cpf,nome,email] in reader:
                    params = {
                        "alias": cpf,
                        "name":nome,
                        "passwd": "Doe123",
                        "usrgrps": [
                            {"usrgrpid": "44"}
                        ],
                        "user_medias": [
                            { 
                                "mediatypeid": "1",
                                "sendto": [email],
                                "active": 0,
                            }
                        ]
                    }
                    print("Incluindo o usuario ",nome,"!")
                    print(self.zabbix_api(method, params))
            except csv.Error as e:
                sys.exit('ficheiro %s, linha %d: %s' % (nome_ficheiro, reader.line_num, e))
        
    
    def zabbix_api(self,method="apiinfo.version", params= {}):
        self.request_object["params"] = params
        self.request_object["method"] = method
        self.id+=1
        self.request = requests.post(self.url+"/api_jsonrpc.php", headers=self.headers , json=self.request_object, verify=False )
        data = loads(self.request.text)
        self.request_object["params"] = {}
        self.request_object["method"] = "apiinfo.version"
        self.request_object["id"] = self.id 
        return data


if __name__ == '__main__':
    urllib3.disable_warnings()
    add = AddUser()
    add.add_multiplos_users()



