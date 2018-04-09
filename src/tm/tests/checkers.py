from datetime import date, timedelta

from django.test import TestCase

from tm.checkers import (
    get_age, gte, lte, equal, not_in, check_flag, check_mortgage,
    check_acc_for_years, PreChecker, CallCreditChecker
)
from tm.models import Setting


def date_minus(days):
    return (date.today() - timedelta(days)).strftime('%Y-%m-%d')


class MainTest(TestCase):
    def test_get_age(self):
        bd = date.today() - timedelta(365*10)
        self.assertEqual(get_age(bd), 9)
        bd = date.today() - timedelta(365*10 + 10)
        self.assertEqual(get_age(bd), 10)

    def test_gte(self):
        self.assertTrue(gte(1, 1))
        self.assertTrue(gte(2, 1))
        self.assertFalse(gte(0, 1))

    def test_lte(self):
        self.assertTrue(lte(1, 1))
        self.assertTrue(lte(0, 1))
        self.assertFalse(lte(2, 1))

    def test_equal(self):
        self.assertTrue(equal(1, 1))
        self.assertFalse(equal(0, 1))
        self.assertFalse(equal(2, 1))

    def test_not_in(self):
        banned = 'one, three '
        self.assertFalse(not_in('one', banned))
        self.assertTrue(not_in('two', banned))
        self.assertFalse(not_in('three', banned))

    def test_check_flag(self):
        self.assertTrue(check_flag(True, False))
        self.assertTrue(check_flag(False, False))
        self.assertTrue(check_flag(False, True))
        self.assertFalse(check_flag(True, True))

    def test_check_mortgage(self):
        data = {
            'acc': [{
                'accdetails': {
                    'accgroupid': 2,
                }
            }, {
                'accdetails': {
                    'accgroupid': 2,
                    'status': 'Q',
                },
            }]
        }
        self.assertFalse(check_mortgage(data))
        data = {
            'acc': [{
                'accdetails': {
                    'accgroupid': 2,
                }
            }, {
                'accdetails': {
                    'status': 'Q',
                },
            }]
        }
        self.assertTrue(check_mortgage(data))

    def test_check_acc_for_years(self):
        data = {
            'acc': [{
                'accdetails': {'accstartdate': date_minus(365 * 3)},
            }, {
                'accdetails': {'accstartdate': date_minus(30 * 36)},
            }]
        }
        self.assertFalse(check_acc_for_years(data, 2))
        data = {
            'acc': [{
                'accdetails': {'accstartdate': date_minus(365 * 3)},
            }, {
                'accdetails': {'accstartdate': date_minus(30 * 20)},
            }]
        }
        self.assertTrue(check_acc_for_years(data, 2))


class Dummy():
    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)


class CheckerTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.setting = Setting.objects.create(is_active=True)

    def test_pre_checker(self):
        # correct data
        data = {
            'date_of_birth': date.today() - timedelta(365*30),
            'income': 2500,
            'loan_amount': 1000,
            'employer_name': 'company',
            'employment_status': 1,
            'occupation': 'ceo',
            'addr_postcode': '12 345',
        }
        self.assertFalse(PreChecker().check(Dummy(**data)))
        # wrong data
        data = {
            'date_of_birth': date.today() - timedelta(365*70),
            'income': 500,
            'loan_amount': 30000,
            'employer_name': 'company',
            'employment_status': 1,
            'addr_postcode': '12 345',
        }
        expect = ['age_max', 'income_min', 'loan_amount_max', 'occupation']
        self.assertEqual(PreChecker().check(Dummy(**data)), expect)

        # banned data
        self.setting.employer = 'badcomp,verybadcomp'
        self.setting.occupation = 'programmer'
        self.setting.postcode = '12345,43215'
        self.setting.save()
        data = {
            'date_of_birth': date.today() - timedelta(365*30),
            'income': 2500,
            'loan_amount': 1000,
            'employer_name': 'verybadcomp',
            'occupation': 'designer',
            'employment_status': 1,
            'addr_postcode': '43215',
        }
        expect = ['employer', 'postcode']
        self.assertEqual(PreChecker().check(Dummy(**data)), expect)

    def test_call_credit(self):
        # wrong data and settings
        self.setting.credit_score_min = 100
        self.setting.indebt_min = 2000
        self.setting.save()
        data = {
            'credit_score': 50,
            'indebt': 500,
            'active_bunkruptcy': True,
            'accs': {
                'acc': [{
                    'accdetails': {
                        'accgroupid': '2',
                        'status': 'Q',
                        'accstartdate': date_minus(365 * 3 + 60),
                    },
                }],
            },
        }
        expect = [
            'credit_score_min', 'credit_score_min_no_mortgage', 'indebt_min',
            'delinquent_mortgage', 'active_bunkruptcy', 'acc_for_years'
        ]
        self.assertEqual(CallCreditChecker().check(Dummy(**data)), expect)

        # wrong data and settings
        self.setting.active_bunkruptcy = False
        self.setting.save()
        data = {
            'credit_score': 480,
            'indebt': 3500,
            'active_bunkruptcy': True,
            'accs': {
                'acc': [{
                    'accdetails': {
                        'accgroupid': '2',
                        'accstartdate': date_minus(365 * 3),
                    },
                }, {
                    'accdetails': {
                        'status': 'Q',
                        'accstartdate': date_minus(365 * 2),
                    },
                }],
            },
        }
        expect = ['credit_score_min_no_mortgage']
        self.assertEqual(CallCreditChecker().check(Dummy(**data)), expect)

        # correct data
        data['accs']['acc'][0]['accdetails']['status'] = 'N'
        self.assertFalse(CallCreditChecker().check(Dummy(**data)))
