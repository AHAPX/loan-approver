import requests
from django.conf import settings


class SMSError(Exception):
    pass


def send_sms(phone, message):
    username = settings.SMS['username']
    password = settings.SMS['password']
    url = f'https://www.2sms.com/xml/sendsms.aspx?username={username}&password={password}&mobile={phone}&sms={message}'
    resp = requests.get(url)
    if resp.status_code != 200:
        raise SMSError(f'sms send error: {resp.content} ({resp.status_code})')
