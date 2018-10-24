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

airport = 'ESSA'
if get_metar_with_negative_temp(airport):
    msg = EmailMessage()
    msg.set_content(''.join(['Check ATIS for : ', airport]))

    msg['Subject'] = 'Record ATIS!'
    msg['From'] = 'monkey@prodrigues.tk'
    msg['To'] = 'prodrigues1990@gmail.com'

    s = smtplib.SMTP('localhost')
    s.send_message(msg)
    s.quit()
