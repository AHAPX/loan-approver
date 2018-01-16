from datetime import date


import logging
logger = logging.getLogger(__name__)


class BaseField():
    pass


class DateField(BaseField):
    def __init__(self, year, month, day=None):
        self.year = year
        self.month = month
        self.day = day

    def convert(self, data):
        year = data.get(self.year)
        month = data.get(self.month)
        day = None
        if self.day:
            day = data.get(self.day)
        day = day or 1
        try:
            return date(int(year), int(month), int(day))
        except:
            return None
        

SUBMIT_FIELDS = {
    'auth_code': 'auth',
    'loan_amount': 'la',
    'title': 't',
    'first_name': 'fn',
    'last_name': 'ln',
    'date_of_birth': DateField('doby', 'dobm', 'dobd'),
    'phone_landline': 'hp',
    'phone_mobile': 'mp',
    'email': 'em',
    'marital_status': 'ms',
    'dependents': 'dep',
    'residential_status': 'rs',
    'rent_mortgage': 'mmr',
    'addr_since': DateField('dmiy', 'dmim'),
    'addr_addr': 'a1',
    'addr_city': 'tn',
    'addr_country': 'ct',
    'addr_postcode': 'pc',
    'employment_status': 'es',
    'employer_name': 'en',
    'occupation': 'oc',
    'employee_since': DateField('osdy', 'osdm'),
    'employment_payment': 'pm',
    'income': 'mi',
    'bank_next_pay_date': DateField('npdy', 'npdm', 'npdd'),
    'addr2_since': DateField('pdmim', 'pdmiy'),
    'addr2_addr': 'pa1',
    'addr2_city': 'ptn',
    'addr2_country': 'pct',
    'addr2_postcode': 'ppc',
    'reference_id': 'affref',
}


def convert(data, convertor):
    result = {}
    for key, field in convertor.items():
        if isinstance(field, BaseField):
            value = field.convert(data)
        else:
            value = data.get(field)
        if value:
            result[key] = value
    return result
