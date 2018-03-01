import requests
from django.conf import settings


class SMSError(Exception):
    pass


def sendSMS(phone, message):
    url = f'https://www.2sms.com/xml/sendsms.aspx?username={settings.SMS_USERNAME}&password={settings.SMS_PASSWORD}&mobile={phone}&sms={message}'
    resp = requests.get(url)
    if resp.status_code != 200:
        raise SMSError(f'sms send error: {resp.content} ({resp.status_code})')
