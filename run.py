#!/usr/bin/python3
import requests
import smtplib
from email.message import EmailMessage

def get_metar_with_negative_temp(airport):
    resp = requests.get('/'.join(['https://avwx.rest/api/metar', airport]))
    metar = resp.json()

    if 'Temperature' in metar:
        temp = int(metar['Temperature'].replace('M', '-'))
    else:
        temp = 1

    if 'Dewpoint' in metar:
        dwpt = int(metar['Dewpoint'].replace('M', '-'))
    else:
        dwpt = 1

    if 'Wind-Speed' in metar:
        windspeed = int(metar['Wind-Speed'])
    else:
        windspeed = 0

    if 'Wind-Gust' in metar:
        if metar['Wind-Gust'] != '':
            windgust = int(metar['Wind-Gust'])
        else:
            windgust = 0
    else:
        windgust = 0

    if (temp <= 0 or dwpt <= 0 or windspeed >= 30 or windgust >= 30):
        return metar['Raw-Report']

airports = ['LPPT', 'LPPR', 'LPFR', 'LPMA', 'LPCS']
alert = []

for airport in airports:
    metar = get_metar_with_negative_temp(airport)
    if metar:
        alert.append(metar)

if alert:
    msg = EmailMessage()
    msg.set_content('\r\n'.join(['Alert triggered for metars : ', *alert]))

    msg['Subject'] = 'METAR Alert!'
    msg['From'] = 'monkey@server.home'
    msg['To'] = 'tmavicente@gmail.com', 'ricardojslourenco@gmail.com'

    s = smtplib.SMTP('localhost')
    s.send_message(msg)
    s.quit()
