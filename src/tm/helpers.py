from io import BytesIO
import os
import random
import string
from urllib.parse import urljoin

from django.conf import settings
from django.db.models import Max
from xhtml2pdf import pisa


SYMBOLS = string.ascii_letters + string.digits


def gen_token(length=8):
    return ''.join([random.choice(SYMBOLS) for i in range(length)])


def gen_pin(length=4):
    return ''.join([random.choice(string.digits) for i in range(length)])


def get_full_url(url):
    return urljoin(settings.MAIN_URL, url)


def get_customer_products(token):
    return get_full_url(f'{settings.CUSTOMER_URL}?code={token}')


def get_customer_sign(token):
    return get_full_url(f'{settings.CUSTOMER_SIGN_URL}?code={token}')


def save_document(text):
    filename = os.path.join(settings.DOCUMENT_DIR, f'agreement_{gen_token()}.pdf')
    pdf = BytesIO()
    pisa.CreatePDF(text, pdf)
    rendered = pdf.getvalue()
    pdf.close()
    open(filename, 'w').write(rendered.decode('utf-8', 'ignore'))
    return filename


def get_template(template):
    from tm.models import Template

    try:
        return Template.objects.get(usefor=template).text
    except:
        return ''


def gen_reference_num():
    from tm.models import Applicant

    try:
        data = Applicant.objects.all().aggregate(Max('reference_number'))
        return data['reference_number__max'] + 1
    except:
        return settings.FIRST_REFERENCE_NUMBER


def number(value, default=0):
    return float(value or default)
