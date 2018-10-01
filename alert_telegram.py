import json
from json import loads
import requests
import datetime
import sys
from PIL import Image
from io import BytesIO
class alertTelegram:
      def __init__(self):
            self.url = "http://10.10.10.101/zabbix/"
            self.cookies = requests.post(self.url, data={"name":"Manute","password":"zabbix","autologin":1,"enter":"Sign in"}).cookies
            print(self.cookies)
            self.get_grafico(self.cookies)

      #Metodo que fazar conexão do usuario
      def conection(self, method ):
            pass
      #Metodo que busca o ID do host que deve ser usado durante a manutenção
      def get_grafico(self,cookies):
            grafico =requests.get("http://10.10.10.101/zabbix/chart.php?period=3600&itemids=23299",cookies=cookies).content
            with open('image_name.jpg', 'wb') as handler:
                  handler.write(grafico)
            
#Iniciando
if __name__ == '__main__':
      #host_name = sys.argv[1]
      manute=alertTelegram()