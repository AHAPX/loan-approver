from datetime import date

from django.test import TestCase

from tm.convertors import (
    extract, get_text, DateField, BaseResponseField, ApplicantConvertor,
    CallCreditConvertor
)


class MainTest(TestCase):
    def test_extract(self):
        data = {
            'a1': {
                'a2': 1,
                'b2': 2,
            },
            'b1': None,
            'c1': {
                'a2': {'a3': 3},
                'b2': None,
            }
        }
        self.assertEqual(extract(data, 'a1.a2'), 1)
        self.assertEqual(extract(data, 'b1.a2'), None)
        self.assertEqual(extract(data, 'c1.a2.a3'), 3)
        self.assertEqual(extract(data, 'c1.a2.b3'), None)

    def test_get_text(self):
        data = {
            'value': 1,
            '#text': 2,
            'text': 3,
        }
        self.assertEqual(get_text(data), 2)


class FieldTest(TestCase):
    def test_date(self):
        # with day
        data = {
            'year': 2018,
            'month': 1,
            'day': 15
        }
        field = DateField('year', 'month', 'day')
        value = field.convert(data)
        self.assertEqual(value, date(2018, 1, 15))
        # without day
        data = {
            'year': 2018,
            'month': 1,
        }
        field = DateField('year', 'month')
        value = field.convert(data)
        self.assertEqual(value, date(2018, 1, 1))
        # error
        data = {
            'year': 'sdfa',
            'month': 1,
        }
        field = DateField('year', 'month')
        value = field.convert(data)
        self.assertEqual(value, None)

    def test_base_response(self):
        data = {
            's:Envelope': {
                's:Body': {
                    'SearchResponse': {
                        'SearchResult': {
                            'ProductResponses': {
                                'base': {
                                    'a1': {
                                        'a2': 1,
                                        'b2': 2,
                                    },
                                    'b1': {
                                        'a2': 3,
                                        'b2': 4,
                                    },
                                },
                            },
                        },
                    },
                },
            },
        }
        # without formattors
        field = BaseResponseField('a1.b2')
        value = field.convert(data)
        self.assertEqual(value, 2)
        # with formattors
        f1 = lambda a: a**2
        f2 = lambda a: a*10
        field = BaseResponseField('b1.b2', f1, f2)
        value = field.convert(data)
        self.assertEqual(value, 160)


class ConvertorTest(TestCase):
    def test_applicant(self):
        data = {
            'auth': 'auth',
            'la': 1000,
            't': 4,
            'fn': 'tester',
            'ln': 'mctest',
            'doby': 1980,
            'dobm': 1,
            'dobd': 19,
            'hp': '0123456789',
            'mp': '0234567891',
            'em': 'test@gmail.com',
            'ms': 1,
            'dep': 2,
            'rs': 1,
            'mmr': 3,
            'dmiy': 2016,
            'dmim': 5,
            'a1': '46,street',
            'tn': 'town',
            'ct': 'GB',
            'pc': '12 345',
            'es': 1,
            'en': 'test company',
            'oc': 'ceo',
            'osdy': 2016,
            'osdm': 10,
            'pm': 1,
            'mi': 6000,
            'npdy': 2015,
            'npdm': 12,
            'npdd': 15,
            'pdmiy': 2010,
            'pdmim': 11,
            'pa1': '32,street',
            'ptn': 'town2',
            'pct': 'UK',
            'ppc': '324 12',
            'affref': '1234567',
        }
        expect = {
            'auth_code': 'auth',
            'loan_amount': 1000,
            'title': 4,
            'first_name': 'tester',
            'last_name': 'mctest',
            'date_of_birth': date(1980, 1, 19),
            'phone_landline': '0123456789',
            'phone_mobile': '0234567891',
            'email': 'test@gmail.com',
            'marital_status': 1,
            'dependents': 2,
            'residential_status': 1,
            'rent_mortgage': 3,
            'addr_since': date(2016, 5, 1),
            'addr_addr': '46,street',
            'addr_city': 'town',
            'addr_country': 'GB',
            'addr_postcode': '12 345',
            'employment_status': 1,
            'employer_name': 'test company',
            'occupation': 'ceo',
            'employee_since': date(2016, 10, 1),
            'employment_payment': 1,
            'income': 6000,
            'bank_next_pay_date': date(2015, 12, 15),
            'addr2_since': date(2010, 11, 1),
            'addr2_addr': '32,street',
            'addr2_city': 'town2',
            'addr2_country': 'UK',
            'addr2_postcode': '324 12',
            'reference_id': '1234567',
        }
        value = ApplicantConvertor().convert(data)
        self.assertEqual(value, expect)

    def test_call_credit(self):
        data = {
            's:Envelope': {'s:Body': {'SearchResponse': {'SearchResult': {'ProductResponses': {
                'BSBAndCreditReport7': {'BSBAndCreditReport7Response': {'Response': {
                    'creditreport': {'applicant': {
                        'creditscores': {'creditscore': {'score': {
                            '#text': '35',
                            'value': '60',
                        }}},
                        'summary': {
                            'indebt': {'totallimitsrevolve': '10'},
                            'share': {'totaldelinqs12months': '22'},
                        },
                    }}}}},
                'AffordabilityReport2': {'AffordabilityReport2Response': {'Response': {'results': {
                    'debtsummary': {'turnoverpercentiles': {
                        'ratioincomechg12': '111',
                        'ratioincomechg3': '234',
                    }}
                }}}},
            }}}}},
        }
        expect = {
            'credit_score': 35,
            'indebt_min': 10.0,
            'delinquent_mortgage': 22,
            'debt_in_income_min': 111,
            'debt_in_income_max': 234,
        }
        value = CallCreditConvertor().convert(data)
        self.assertEqual(value, expect)
