#!/usr/bin/python3
import requests
import smtplib
from email.message import EmailMessage

def get_metar_with_negative_temp(airport):
    resp = requests.get('/'.join(['https://avwx.rest/api/metar', airport]))
    metar = resp.json()

    temp = int(metar['Temperature'].replace('M', '-'))
    dwpt = int(metar['Dewpoint'].replace('M', '-'))

    if (temp < 0 or dwpt < 0):
        return metar['Raw-Report']

airports = ['LPPT', 'LPPR', 'LPFR', 'LPMA']
alert = []

for airport in airports:
    metar = get_metar_with_negative_temp(airport)
    if metar:
        alert.append(metar)

if alert:
    msg = EmailMessage()
    msg.set_content('\r\n'.join(['Alert triggered for metars : ', *alert]))

    msg['Subject'] = 'METAR Alert!'
    msg['From'] = 'monkey@prodrigues.tk'
    msg['To'] = 'prodrigues1990@gmail.com'

    s = smtplib.SMTP('localhost')
    s.send_message(msg)
    s.quit()
