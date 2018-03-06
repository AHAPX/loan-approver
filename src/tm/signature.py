import base64

from django.conf import settings
from django.template.loader import render_to_string
import requests
import xmltodict


def create_url_widget(filename, https, site, lrn):
    body = open(filename).read().encode()
    context = {
        'api_key': settings.ECHOSIGN_API_KEY,
        'file': base64.b64encode(body),
        'filename': filename,
        'redirect': f'http{"s" if https else ""}://{site}/s/{lrn}',
    }
    body = render_to_string('sign_widget.xml', context)
    response = requests.post(
        settings.ECHOSIGN_API_URL,
        data=body,
        headers={
            'Content-Type'  : 'text/xml; charset=UTF-8',
            'SOAPAction'    : '""'
        }
    )
    data = xmltodict.parse(response.text)
    try:
        return data['soap:Envelope']['soap:Body']['ns1:createUrlWidgetResponse']\
            ['ns1:urlWidgetCreationResult']['url']['#text']
    except:
        raise
