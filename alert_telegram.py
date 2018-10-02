#!/usr/bin/env python
# -*- coding: utf-8 -*-
import requests
import sys
from PIL import Image
from io import BytesIO
class alertTelegram:
      def __init__(self, send_user, msg, item_id):
            token = "681206017:AAFVw6H0d9Aitr6V2wlMGYqdU6tK3CwZTkA"
            self.url = "http://10.10.10.101/zabbix/"
            self.send_user = send_user
            self.msg = msg
            self.item_id = item_id
            self.send_msg(send_user , msg,token)
            #self.get_grafico(self.cookies)
      #Metodo que busca o ID do host que deve ser usado durante a manutenção
      def get_grafico(self,item_id):
            cookies = requests.post(self.url, data={"name":"Manute","password":"zabbix","autologin":1,"enter":"Sign in"}).cookies
            grafico =requests.get("http://10.10.10.101/zabbix/chart.php?period=1800&itemids="+item_id,cookies=cookies).content
            with open('/tmp/alerta.jpg', 'wb') as handler:
                  handler.write(grafico)
      def send_msg(self, send_user,msg, token):
            payload = {"chat_id": send_user, "text": msg,"parse_mode":"HTML"}
            r = requests.get('https://api.telegram.org/bot'+token+"/sendMessage", params=payload)
            

#Iniciando
if __name__ == '__main__':
      send_user = str(sys.argv[1])
      msg = str(sys.argv[2])
      item_id = str(sys.argv[3])
      manute=alertTelegram(send_user,msg,item_id)
      #print(send_user)
      #print(subject)

      '''with open('nomes.txt', 'a') as arq:
            arq.write(send_user)
            arq.write('\n')
            arq.write(subject)
            arq.write('\n')
            arq.write(mensagem)
            arq.close
      #'''