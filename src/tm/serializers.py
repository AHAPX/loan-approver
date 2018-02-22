from rest_framework import serializers

from .models import Applicant, Introducer, Template
from .consts import EMPLOYMENT_CHOICES


class ApplicantSerializer(serializers.ModelSerializer):
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
