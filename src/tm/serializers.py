from django.contrib.auth.models import User
from rest_framework import serializers

from .models import Applicant, Introducer, Template, Product
from .consts import EMPLOYMENT_CHOICES


class SubmitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Applicant
        fields = (
            'id', 'introducer', 'loan_amount', 'title', 'first_name', 'last_name',
            'date_of_birth', 'phone_landline', 'phone_mobile', 'email',
            'marital_status', 'dependents', 'residential_status', 'rent_mortgage',
            'addr_since', 'addr_city', 'addr_country', 'addr_postcode',
            'employment_status', 'employer_name', 'occupation', 'employee_since',
            'employment_payment', 'income', 'bank_next_pay_date', 'addr2_since',
            'addr2_city', 'addr2_country', 'addr2_postcode', 'reference_id',
        )


class ApplicantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Applicant
        fields = (
            'id', 'introducer', 'loan_amount', 'loan_term', 'loan_purpose',
            'title', 'first_name', 'last_name', 'date_of_birth', 'sex',
            'phone_landline', 'phone_mobile', 'email', 'dependents',
            'residential_status', 'live_with', 'rent_mortgage', 'marital_status',
            'adults', 'children', 'cars', 'partner_income', 'partner_contrib',
            'child_care_costs',
            'addr_flat', 'addr_house_name', 'addr_house_number', 'addr_street',
            'addr_city', 'addr_country', 'addr_postcode', 'addr_since',
            'addr_electral_roll', 'addr_credit',
            'addr2_flat', 'addr2_house_name', 'addr2_house_number', 'addr2_street',
            'addr2_city', 'addr2_country', 'addr2_postcode', 'addr2_since',
            'employment_status', 'employer_name', 'occupation', 'employer_address',
            'employee_since', 'employment_payment', 'job_title', 'income',
            'income_split', 'nin',
            'bank_sort_code', 'bank_account_number', 'bank_pay_frequency',
            'bank_next_pay_date', 'no_dd', 'reference_id',
        )


class IntroducerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Introducer
        fields = (
            'id', 'auth_code', 'ip', 'netmask', 'name', 'address', 'website',
            'phone', 'is_active',
        )


class TemplateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Template
        fields = ('id', 'name', 'text', 'usefor')


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'id', 'username', 'first_name', 'last_name', 'email', 'password',
            'is_active', 'is_staff', 'is_superuser', 'user_permissions',
        )


class SettingSerializer(serializers.Serializer):
    age_max = serializers.IntegerField(required=False)
    age_min = serializers.IntegerField(required=False)
    employment_status = serializers.IntegerField(required=False)
    income_min = serializers.FloatField(required=False)
    loan_amount_min = serializers.FloatField(required=False)
    loan_amount_max = serializers.FloatField(required=False)
    employer = serializers.BooleanField(required=False)
    occupation = serializers.BooleanField(required=False)
    postcode = serializers.BooleanField(required=False)

    def save(self):
        fields = (
            'age_max', 'age_min', 'employment_status', 'income_min',
            'loan_amount_min', 'loan_amount_max', 'employer',
            'occupation', 'postcode',
        )
        for field in fields:
            value = getattr(self.instance, field, None)
            setattr(self.instance, field, self.validated_data.get(field, value))
        self.instance.save()
        return self.instance


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = (
            'introducer', 'group', 'amount', 'term', 'annual_rate',
            'annual_percentage_rate', 'payment', 'mask', 'interest',
            'total_charge', 'total_payable', 'default_interest',
            'daily_interest', 'min_score_tenant', 'min_in_debt',
            'min_score_mtg', 'is_active',
        )
