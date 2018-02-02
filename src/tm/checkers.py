from datetime import date

from .models import Setting


def get_age(dt):
    today = date.today()
    return today.year - dt.year - ((today.month, today.day) < (dt.month, dt.day))


def gte(value1, value2):
    return value1 >= value2


def lte(value1, value2):
    return value1 <= value2


def equal(value1, value2):
    return value1 == value2


class PreChecker():
    rules = {
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
            'format': bool,
            'check': equal,
        },
        'employment_status': {
            'field': 'employment_status',
            'check': equal,
        },
        'occupation': {
            'field': 'occupation',
            'format': bool,
            'check': equal,
        },
        'postcode': {
            'field': 'addr_postcode',
            'format': bool,
            'check': equal,
        },
    }

    def check(self, applicant):
        errors = []
        for key, rule in self.rules.items():
            setting = Setting.get_setting(key)
            setting_value = setting.get_value()
            if setting_value is None:
                continue
            field = rule['field']
            value = hasattr(applicant, field) and getattr(applicant, field)
            if rule.get('format'):
                value = rule['format'](value)
            if not rule['check'](value, setting_value):
                errors.append(setting.name)
        return errors
