from datetime import date, datetime, timedelta
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


def check_flag(flag, checker):
    return not checker or not flag


def check_mortgage(accs, *args):
    for acc in accs.get('acc', []):
        details = acc.get('accdetails', {})
        if int(details.get('accgroupid', 0)) == 2 and details.get('status') == 'Q':
            return False
    return True


def check_acc_for_years(accs, years):
    last_date = datetime.today() - timedelta(365 * years)
    for acc in accs.get('acc', []):
        details = acc.get('accdetails', {})
        try:
            start_date = datetime.strptime(details.get('accstartdate'), '%Y-%m-%d')
        except:
            continue
        if start_date > last_date:
            return True
    return False


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

RULES_CALL_CREDIT = {
    'credit_score_min': {
        'field': 'credit_score',
        'check': gte,
    },
    'indebt_min': {
        'field': 'indebt',
        'check': gte,
    },
    'delinquent_mortgage': {
        'field': 'accs',
        'check': check_mortgage,
    },
    'active_bunkruptcy': {
        'field': 'active_bunkruptcy',
        'check': check_flag,
    },
    'acc_for_years': {
        'field': 'accs',
        'check': check_acc_for_years,
    },
}


class BaseChecker():
    rules = {}

    def check(self, item):
        errors = []
        for key, rule in self.rules.items():
            setting = Setting.get_setting()
            setting_value = getattr(setting, key, None)
#            if setting_value is None:
#                continue
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
