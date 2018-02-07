import requests

from django.template.loader import render_to_string
from django.conf import settings
import xmltodict


def search_request(applicant):
    callcredit = settings.CALL_CREDIT['test']
    context = {
        'applicant': applicant,
        'callcredit': callcredit,
    }
    body = render_to_string('search.xml', context)
    response = requests.post(
        callcredit['url'],
        data=body,
        headers=callcredit['headers'],
        proxies=callcredit.get('proxies', {})
    )
    return xmltodict.parse(response.text)
