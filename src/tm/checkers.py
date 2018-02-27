from datetime import date
import logging
import requests

from django.template.loader import render_to_string
from django.conf import settings
import xmltodict

from .models import Setting


logger = logging.getLogger(__name__)


def get_age(dt):
    today = date.today()
    return today.year - dt.year - ((today.month, today.day) < (dt.month, dt.day))


def gte(value1, value2):
    return value1 >= value2


def lte(value1, value2):
    return value1 <= value2


def equal(value1, value2):
    return value1 == value2


def not_in(value1, value2):
    if isinstance(value2, str):
        value2 = [x.strip().lower() for x in value2.split(',')]
    return value1.lower() not in value2


RULES_PRE = {
    'age_min': {
        'field': 'date_of_birth',
        'format': get_age,
        'check': gte,
    },
    'age_max': {
        'field': 'date_of_birth',
        'format': get_age,
        'check': lte,
    },
    'income_min': {
        'field': 'income',
        'check': gte,
    },
    'loan_amount_min': {
        'field': 'loan_amount',
        'check': gte,
    },
    'loan_amount_max': {
        'field': 'loan_amount',
        'check': lte,
    },
    'employer': {
        'field': 'employer_name',
        'format': str,
        'check': not_in,
    },
    'employment_status': {
        'field': 'employment_status',
        'check': equal,
    },
    'occupation': {
        'field': 'occupation',
        'format': str,
        'check': not_in,
    },
    'postcode': {
        'field': 'addr_postcode',
        'format': str,
        'check': not_in,
    },
}

# TODO: not correct rules, just for test, need to be change
RULES_CALL_CREDIT = {
    'credit_score_min': {
        'field': 'credit_score',
        'check': gte,
    },
    'credit_score_with_mortgage_min': {
        'field': 'credit_score_with_mortgage',
        'check': gte,
    },
    'indebt_min': {
        'field': 'indebt_min',
        'check': gte,
    },
    'delinquent_mortgage': {
        'field': 'delinquent_mortgage',
        'format': bool,
        'check': equal,
    },
    'active_bunkruptcy': {
        'field': 'active_bunkruptcy',
        'format': bool,
        'check': equal,
    },
    'debt_in_income_min': {
        'field': 'debt_in_income_min',
        'check': gte,
    },
    'debt_in_income_max': {
        'field': 'debt_in_income_max',
        'check': lte,
    },
    'last_credit': {
        'field': 'last_credit',
        'check': gte,
    },
}



class BaseChecker():
    rules = {}

    def check(self, item):
        errors = []
        for key, rule in self.rules.items():
            setting = Setting.get_setting()
            setting_value = getattr(setting, key, None)
            if setting_value is None:
                continue
            field = rule['field']
            value = getattr(item, field, None)
            if value == None:
                errors.append(key)
                continue
            if rule.get('format'):
                value = rule['format'](value)
            if not rule['check'](value, setting_value):
                errors.append(key)
        return errors


class PreChecker(BaseChecker):
    rules = RULES_PRE


class CallCreditChecker(BaseChecker):
    rules = RULES_CALL_CREDIT
