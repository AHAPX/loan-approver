from rest_framework.serializers import ModelSerializer

from .models import Applicant


class ApplicantSerializer(ModelSerializer):
    class Meta:
        model = Applicant
        fields = (
            'introducer', 'loan_amount', 'title', 'first_name', 'last_name',
            'date_of_birth', 'phone_landline', 'phone_mobile', 'email',
            'marital_status', 'dependents', 'residential_status', 'rent_mortgage',
            'addr_since', 'addr_city', 'addr_country', 'addr_postcode',
            'employment_status', 'employer_name', 'occupation', 'employee_since',
            'employment_payment', 'income', 'bank_next_pay_date', 'addr2_since',
            'addr2_city', 'addr2_country', 'addr2_postcode', 'reference_id',
        )
