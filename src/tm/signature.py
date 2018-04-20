import logging
import base64

from django.conf import settings
from django.template.loader import render_to_string
import requests
import xmltodict


logger = logging.getLogger(__name__)


def create_url_widget(filename, url):
    body = open(filename, encoding='iso-8859-1').read().encode()#'iso-8859-1')
    context = {
        'api_key': settings.ECHOSIGN_API_KEY,
        'file': base64.b64encode(body),
        'filename': filename,
        'redirect': url,
    }
    data = render_to_string('sign_widget.xml', context)
    response = requests.post(
        settings.ECHOSIGN_API_URL,
        data=data.strip(),
        headers={
            'Content-Type'  : 'text/xml; charset=UTF-8',
            'SOAPAction'    : '""'
        }
    )
    resp = xmltodict.parse(response.text)
    try:
        return resp['soap:Envelope']['soap:Body']['ns1:createUrlWidgetResponse']\
            ['ns1:urlWidgetCreationResult']['url']['#text']
    except:
        logging.getLogger(__name__).error(resp)
        raise
