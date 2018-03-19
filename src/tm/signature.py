import logging
import base64

from django.conf import settings
from django.template.loader import render_to_string
import requests
import xmltodict


logger = logging.getLogger(__name__)


def create_url_widget(filename, url):
    body = open(filename).read().encode('utf8')
#    logger.warning(body)
    context = {
        'api_key': settings.ECHOSIGN_API_KEY,
        'file': base64.b64encode(body),
        'filename': filename,
        'redirect': url,
    }
#    logger.warning(context)
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
    logging.getLogger(__name__).error(data)
    try:
        return data['soap:Envelope']['soap:Body']['ns1:createUrlWidgetResponse']\
            ['ns1:urlWidgetCreationResult']['url']['#text']
    except:
        raise
