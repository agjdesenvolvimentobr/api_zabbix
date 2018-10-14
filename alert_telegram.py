#!/usr/bin/env python
# -*- coding: utf-8 -*-
import requests
import sys
from PIL import Image
from io import BytesIO
import json
from json import loads

class alertTelegram:
      def __init__(self, send_user, msg, item_id):
            token = "<TOKEN>"
            self.url_ZABBIX = "http://10.10.10.101/zabbix/"
            self.send_msg(send_user , msg,token)
            photo=self.get_grafico(item_id)
            self.send_img(send_user, photo ,token)
      #Metodo que busca o ID do host que deve ser usado durante a manutenção
      def get_grafico(self,item_id):
            cookies = requests.post(self.url_ZABBIX, data={"name":"Manute","password":"zabbix","autologin":1,"enter":"Sign in"}).cookies
            grafico =requests.get(self.url_ZABBIX+"chart.php?period=1800&itemids="+item_id,cookies=cookies).content
            with open('alerta.jpeg', 'wb') as file:
                 file.write(grafico)
                 file.close()
            return 'alerta.jpg'
      def send_msg(self, send_user,msg, token):
            payload = {"chat_id": send_user, "text": msg,"parse_mode":"HTML"}
            r = requests.get('https://api.telegram.org/bot'+token+"/sendMessage", params=payload)
            print(r.text)
      def send_img(self, send_user,photo, token):
            '''bio = BytesIO()
            bio.name = 'alerta.jpeg'
            image.save(bio, 'JPEG')
            bio.seek(0)'''
            f = open("alerta.jpg", "rb")
            payload = {"chat_id": send_user, "photo": f,"parse_mode":"HTML"}
            r = requests.get('https://api.telegram.org/bot'+token+"/sendPhoto", params=payload)
            print(r.text)
#Iniciando
if __name__ == '__main__':
      send_user = str(sys.argv[1])
      msg = str(sys.argv[2])
      item_id = str(sys.argv[3])
      manute=alertTelegram(send_user,msg,item_id)
