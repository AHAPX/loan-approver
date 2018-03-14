import random
import string
from urllib.parse import urljoin

from django.conf import settings
from django.urls import reverse


SYMBOLS = string.ascii_letters + string.digits


def gen_token(length=8):
    return ''.join([random.choice(SYMBOLS) for i in range(length)])


def get_customer_products(token):
    return urljoin(settings.MAIN_URL, reverse('customer_main', kwargs={'token': token}))
