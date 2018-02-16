from datetime import date, timedelta

from django.test import TestCase

from tm.checkers import get_age, gte, lte, equal, PreChecker, CallCreditChecker
from tm.models import Setting


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


class DummyApplicant():
    date_of_birth = None
    income = None
    loan_amount = None
    employer_name = None
    employment_status = None
    occupation = None
    addr_postcode = None

    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)


class CheckerTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        setting = Setting.objects.create(is_active=True)

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
        self.assertFalse(PreChecker().check(DummyApplicant(**data)))
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
        self.assertEqual(PreChecker().check(DummyApplicant(**data)), expect)
