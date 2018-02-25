import json
from datetime import date
import os

from django.conf import settings
from django.contrib.auth.models import User
from django.db import models
from django.test import TestCase
from rest_framework.test import APIClient

from tm.models import Applicant, Introducer, Template, Setting


class BaseViewTestMixin():
    auth = {
        'username': 'tester1',
        'password': 'password',
    }

    def get_data(self, name):
        path = os.path.join(settings.BASE_DIR, 'tm/tests/fixtures', name)
        return json.loads(open(f'{path}.json').read())

    @classmethod
    def setUpClass(cls):
        cls.cls_atomics = cls._enter_atomics()
        user = User.objects.create(is_active=True, is_staff=True, is_superuser=True,
            username=cls.auth['username'])
        user.set_password(cls.auth['password'])
        user.save()

    def setUp(self):
        self.assertTrue(self.client.login(**self.auth))


class MainTestsMixin(BaseViewTestMixin):
    fields = ()
    model = None
    url = ''
    new_data = {}
    edit_data = {}
    add = True
    edit = True
    delete = True
    ignore_fields = ()

    def __init__(self, *args, **kwargs):
        if isinstance(self.fields, str):
            self.fields = self.get_data(self.fields)['fields']
        if isinstance(self.new_data, str):
            self.new_data = self.get_data(self.new_data)
        if isinstance(self.edit_data, str):
            self.edit_data = self.get_data(self.edit_data)
        super(MainTestsMixin, self).__init__(*args, **kwargs)

    def test_get(self):
        resp = self.client.get(f'{self.url}')
        self.assertEqual(len(resp.data), self._count)
        item = self.model.objects.create(**self.new_data)
        resp = self.client.get(f'{self.url}')
        self.assertEqual(len(resp.data), self._count + 1)
        for field in self.fields:
            value = getattr(item, field)
            if isinstance(value, models.Model):
                value = value.pk
            if field in self.ignore_fields:
                continue
            self.assertEqual(resp.data[self._count].get(field), value)

    def test_add(self):
        if not self.add:
            return
        resp = self.client.get(f'{self.url}')
        self.assertEqual(len(resp.data), self._count)
        resp = self.client.post(
            f'{self.url}',
            json.dumps(self.new_data),
            content_type='application/json'
        )
        resp = self.client.get(f'{self.url}')
        self.assertEqual(len(resp.data), self._count + 1)
        for field in self.fields:
            if field == 'id':
                continue
            if field in self.ignore_fields:
                continue
            self.assertEqual(resp.data[self._count].get(field), self.new_data.get(field))

    def test_edit_and_delete(self):
        pk = self.model.objects.create(**self.new_data).pk
        resp = self.client.get(f'{self.url}')
        self.assertEqual(len(resp.data), self._count + 1)
        if self.edit:
            # edit record
            resp = self.client.put(
                f'{self.url}{pk}/',
                json.dumps(self.edit_data),
                content_type='application/json'
            )
            for key, value in self.edit_data.items():
                if key in self.ignore_fields:
                    continue
                self.assertEqual(resp.data.get(key), value)
        if self.delete:
            # delete record
            self.client.delete(f'{self.url}{pk}/')
            resp = self.client.get(f'{self.url}')
            self.assertEqual(len(resp.data), self._count)

    def setUp(self):
        self._count = self.model.objects.all().count()
        super(MainTestsMixin, self).setUp()


class IntroducerTest(MainTestsMixin, TestCase):
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


class TemplateTest(MainTestsMixin, TestCase):
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


class SettingTest(BaseViewTestMixin, TestCase):
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


class ApplicantTest(MainTestsMixin, TestCase):
    fields = 'applicant_fields'
    model = Applicant
    url = '/v1/applicants/'
    new_data = 'applicant_new'
    edit_data = 'applicant_edit'
    add = False
    delete = False

    def setUp(self):
        data = {
            'auth_code': 'apikey1234',
            'ip': '127.0.0.1',
            'netmask': '255.255.255.0',
            'name': 'test introducer',
            'address': 'some address',
            'website': 'http://test.com',
            'phone': '0123456789',
            'is_active': True,
        }
        introducer = Introducer.objects.create(**data)
        self.new_data['introducer'] = introducer
        self.edit_data['introducer'] = introducer.pk
        super(ApplicantTest, self).setUp()


class UserTest(MainTestsMixin, TestCase):
    fields = (
        'username', 'first_name', 'last_name', 'email', 'password',
        'is_active', 'is_staff', 'is_superuser', 'user_permissions',
    )
    model = User
    url = '/v1/users/'
    new_data = {
        'username': 'johny',
        'first_name': 'john',
        'last_name': 'smith',
        'email': 'test1@gmail.com',
        'password': 'secret',
        'is_active': True,
        'is_staff': True,
        'is_superuser': False,
    }
    edit_data = {
        'username': 'walter',
        'first_name': 'walter',
        'last_name': 'covacs',
        'email': 'test2@gmail.com',
        'password': 'password',
        'is_active': False,
        'is_staff': False,
        'is_superuser': True,
    }
    delete = False
    ignore_fields = ('user_permissions',)
