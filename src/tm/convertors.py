from datetime import date


import logging
logger = logging.getLogger(__name__)


def extract(data, name):
    if not isinstance(data, dict):
        return None
    names = name.split('.', 1)
    value = data.get(names[0])
    if not value:
        return value
    if len(names) > 1 and isinstance(value, dict):
        value = extract(value, names[1])
    return value


def get_text(data):
    if isinstance(data, dict):
        return data.get('#text')


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


class BaseResponseField(BaseField):
    product = 'base'

    def __init__(self, path, *args):
        self.path = path
        self.product = f's:Envelope.s:Body.SearchResponse.SearchResult.ProductResponses.{self.product}'
        self.formattors = [f for f in args if callable(f)]

    def convert(self, data):
        d = extract(data, self.product)
        value = extract(d, self.path)
        for formattor in self.formattors:
            try:
                value = formattor(value)
            except:
                pass
        return value


class BSBAndCreditField(BaseResponseField):
    product = 'BSBAndCreditReport7.BSBAndCreditReport7Response.Response.creditreport.applicant'


class AffordabilityField(BaseResponseField):
    product = 'AffordabilityReport2.AffordabilityReport2Response.Response.results'


class BaseConvertor():
    fields = {}

    def convert(self, data):
        result = {}
        for key, field in self.fields.items():
            if isinstance(field, BaseField):
                value = field.convert(data)
            else:
                value = data.get(field)
            if value:
                result[key] = value
        return result


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
    'addr2_since': DateField('pdmiy', 'pdmim'),
    'addr2_addr': 'pa1',
    'addr2_city': 'ptn',
    'addr2_country': 'pct',
    'addr2_postcode': 'ppc',
    'reference_id': 'affref',
}


CALL_CREDIT_FIELDS = {
    'credit_score': BSBAndCreditField('creditscores.creditscore.score', get_text, int),
    'indebt_min': BSBAndCreditField('summary.indebt.totallimitsrevolve', float),
    'delinquent_mortgage': BSBAndCreditField('summary.share.totaldelinqs12months', int),
    'debt_in_income_min': AffordabilityField('debtsummary.turnoverpercentiles.ratioincomechg12', float),
    'debt_in_income_max': AffordabilityField('debtsummary.turnoverpercentiles.ratioincomechg3', float),
}


class ApplicantConvertor(BaseConvertor):
    fields = SUBMIT_FIELDS


class CallCreditConvertor(BaseConvertor):
    fields = CALL_CREDIT_FIELDS
