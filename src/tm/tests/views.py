import json
from datetime import date

from django.test import TestCase

from tm.models import Introducer, Template, Setting


class BaseViewTestMixin():
    fields = ()
    model = None
    url = ''
    new_data = {}
    edit_data = {}

    def test_get_and_add(self):
        resp = self.client.get(f'{self.url}')
        self.assertEqual(len(resp.data), 0)
        item = self.model.objects.create(**self.new_data)
        resp = self.client.get(f'{self.url}')
        self.assertEqual(len(resp.data), 1)
        for field in self.fields:
            self.assertEqual(resp.data[0].get(field), getattr(item, field))

    def test_edit_and_delete(self):
        pk = self.model.objects.create(**self.new_data).pk
        resp = self.client.get(f'{self.url}')
        self.assertEqual(len(resp.data), 1)
        resp = self.client.put(
            f'{self.url}{pk}/',
            json.dumps(self.edit_data),
            content_type='application/json'
        )
        item = self.model.objects.get(pk=pk)
        for key, value in self.edit_data.items():
            self.assertEqual(getattr(item, key), value)
        # delete record
        self.client.delete(f'{self.url}{pk}/')
        resp = self.client.get(f'{self.url}')
        self.assertEqual(len(resp.data), 0)


class IntroducerTest(TestCase, BaseViewTestMixin):
    fields = (
        'id', 'auth_code', 'ip', 'netmask', 'name', 'address', 'website', 'phone',
        'is_active',
    )
    model = Introducer
    url = '/v1/introducers/'
    new_data = {
        'auth_code': 'apikey1234',
        'ip': '127.0.0.1',
        'netmask': '255.255.255.0',
        'name': 'test introducer',
        'address': 'some address',
        'website': 'http://test.com',
        'phone': '0123456789',
        'is_active': True,
    }
    edit_data = {
        'auth_code': '3412apikey',
        'ip': '127.0.0.5',
        'netmask': '255.255.255.255',
        'name': 'test intro',
        'address': 'new address',
        'website': 'http://test.io',
        'phone': '9876543210',
        'is_active': False,
    }


class TemplateTest(TestCase, BaseViewTestMixin):
    fields = ('name', 'text', 'usefor')
    model = Template
    url = '/v1/templates/'
    new_data = {
        'name': 'test template',
        'text': 'template body',
        'usefor': 1,
    }
    edit_data = {
        'name': 'test templ',
        'text': 'template new body',
        'usefor': 5,
    }


class SettingTest(TestCase):
    def test_get_and_edit(self):
        new_data = {
            'age_max': 50,
            'age_min': 10,
            'employment_status': 1,
            'income_min': 999,
            'loan_amount_min': 499,
            'loan_amount_max': 2399,
            'employer': True,
            'occupation': True,
            'postcode': True,
        }
        setting = Setting.objects.create(is_active=True, **new_data)
        resp = self.client.get('/v1/settings/')
        self.assertEqual(len(resp.data), len(new_data))
        for key, value in new_data.items():
            self.assertEqual(value, resp.data.get(key))
        # change setting
        edit_data = {
            'age_max': 30,
            'age_min': 28,
            'employment_status': 2,
            'income_min': 500,
            'loan_amount_min': 1000,
            'loan_amount_max': 4000,
            'employer': False,
            'occupation': False,
            'postcode': False,
        }
        resp = self.client.put(
            '/v1/settings/',
            json.dumps(edit_data),
            content_type='application/json'
        )
        resp = self.client.get('/v1/settings/')
        self.assertEqual(len(resp.data), len(edit_data))
        for key, value in edit_data.items():
            self.assertEqual(value, resp.data.get(key))
