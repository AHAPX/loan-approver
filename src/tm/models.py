from django.contrib.postgres.fields import JSONField
from django.db import models

from .consts import (
    STATES, TEMPLATES_CHOICES, SEX_CHOICES, TITLE_CHOICES, MARITAL_CHOICES,
    RESIDENTIAL_CHOICES, EMPLOYMENT_CHOICES, PAYMENT_CHOICES,
    PAY_FREQUENCY_CHOICES, LIVE_WITH_CHOICES, SETTING_TYPE_CHOICES,
    RESULT_CHOICES
)
from .convertors import CallCreditConvertor


class Introducer(models.Model):
    auth_code = models.CharField(max_length=64, null=True, blank=True)
    ip = models.CharField(max_length=15, null=True, blank=True)
    netmask = models.CharField(max_length=15, null=True, blank=True)
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=255, null=True, blank=True)
    website = models.URLField(max_length=100, null=True, blank=True)
    phone = models.CharField(max_length=20, null=True, blank=True)
    is_active = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Template(models.Model):
    name = models.CharField(max_length=100)
    text = models.TextField()
    usefor = models.IntegerField(choices=TEMPLATES_CHOICES)

    def __str__(self):
        return self.name


class Product(models.Model):
    introducer = models.ForeignKey(Introducer, related_name='products', on_delete=models.CASCADE)
    group = models.IntegerField()
    amount = models.FloatField()
    term = models.IntegerField()
    annual_rate = models.FloatField()
    annual_percentage_rate = models.FloatField()
    payment = models.FloatField()
    mask = models.FloatField()
    interest = models.FloatField()
    total_charge = models.FloatField()
    total_payable = models.FloatField()
    default_interest = models.FloatField()
    daily_interest = models.FloatField()
    min_score_tenant = models.IntegerField()
    min_in_debt = models.IntegerField()
    min_score_mtg = models.IntegerField()
    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.introducer}-{self.amount}'


class Applicant(models.Model):
    introducer = models.ForeignKey(Introducer, related_name='applicants', on_delete=models.CASCADE)
    reference_id = models.CharField(max_length=64, null=True, blank=True)

    # personal
    title = models.PositiveSmallIntegerField(choices=TITLE_CHOICES)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    date_of_birth = models.DateField()
    sex = models.CharField(max_length=1, choices=SEX_CHOICES, null=True, blank=True)
    phone_landline = models.CharField(max_length=12, null=True, blank=True)
    phone_mobile = models.CharField(max_length=12)
    email = models.EmailField()
    dependents = models.PositiveSmallIntegerField(null=True, blank=True)

    # loan
    loan_amount = models.DecimalField(decimal_places=2, max_digits=12)
    loan_term = models.PositiveSmallIntegerField(null=True, blank=True)
    loan_purpose = models.TextField(null=True, blank=True)

#    state = models.IntegerField(default=STATES.BEGIN)

    # residential and family
    residential_status = models.PositiveSmallIntegerField(choices=RESIDENTIAL_CHOICES, null=True, blank=True)
    live_with = models.PositiveSmallIntegerField(choices=LIVE_WITH_CHOICES, null=True, blank=True)
    rent_mortgage = models.DecimalField(null=True, blank=True, decimal_places=2, max_digits=12)
    marital_status = models.PositiveSmallIntegerField(choices=MARITAL_CHOICES, null=True, blank=True)
    adults = models.PositiveSmallIntegerField(default=0)
    children = models.PositiveSmallIntegerField(default=0)
    cars = models.PositiveSmallIntegerField(default=0)
    partner_income = models.DecimalField(null=True, blank=True, decimal_places=2, max_digits=12)
    partner_contrib = models.DecimalField(null=True, blank=True, decimal_places=2, max_digits=12)
    child_care_costs = models.DecimalField(null=True, blank=True, decimal_places=2, max_digits=12)

    # current address
    addr_flat = models.CharField(max_length=10, null=True, blank=True)
    addr_house_name = models.CharField(max_length=30, null=True, blank=True)
    addr_house_number = models.CharField(max_length=10, null=True, blank=True)
    addr_street = models.CharField(max_length=30, null=True, blank=True)
    addr_city = models.CharField(max_length=30, null=True, blank=True)
    addr_country = models.CharField(max_length=50, null=True, blank=True)
    addr_postcode = models.CharField(max_length=8, null=True, blank=True)
    addr_since = models.DateField(null=True, blank=True)

    # previous address
    addr2_flat = models.CharField(max_length=10, null=True, blank=True)
    addr2_house_name = models.CharField(max_length=30, null=True, blank=True)
    addr2_house_number = models.CharField(max_length=10, null=True, blank=True)
    addr2_street = models.CharField(max_length=30, null=True, blank=True)
    addr2_city = models.CharField(max_length=50, null=True, blank=True)
    addr2_country = models.CharField(max_length=50, null=True, blank=True)
    addr2_postcode = models.CharField(max_length=8, null=True, blank=True)
    addr2_since = models.DateField(null=True, blank=True)

    # employment details
    employment_status = models.PositiveSmallIntegerField(choices=EMPLOYMENT_CHOICES)
    employer_name = models.CharField(max_length=100, null=True, blank=True)
    occupation = models.CharField(max_length=50, null=True, blank=True)
    employer_address = models.CharField(max_length=100, null=True, blank=True)
    employee_since = models.DateField(null=True, blank=True)
    employment_payment = models.PositiveSmallIntegerField(choices=PAYMENT_CHOICES, null=True, blank=True)
    job_title = models.CharField(max_length=50, null=True, blank=True)
    income = models.DecimalField(null=True, blank=True, decimal_places=2, max_digits=12)
    income_split = models.DecimalField(null=True, blank=True, decimal_places=2, max_digits=12)
    nin = models.CharField(max_length=12, null=True, blank=True)

#    employer_city = models.CharField(max_length=50, null=True, blank=True)
#    employer_county = models.CharField(max_length=50, null=True, blank=True)
#    employer_postcode = models.CharField(max_length=8, null=True, blank=True)
#    employer_phone = models.CharField(max_length=20, null=True, blank=True)
#    hours_per_week = models.PositiveSmallIntegerField(null=True, blank=True)

    # bank details
    bank_sort_code = models.CharField(max_length=6, null=True, blank=True)
    bank_account_number = models.CharField(max_length=20, null=True, blank=True)
    bank_pay_frequency = models.PositiveSmallIntegerField(choices=PAY_FREQUENCY_CHOICES, null=True, blank=True)
    bank_next_pay_date = models.DateField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'


class CallCredit(models.Model):
    # full response
    applicant = models.ForeignKey(Applicant, related_name='callcredits', on_delete=models.CASCADE)
    data = JSONField()

    # QS report
    credit_score = models.IntegerField(null=True)
    credit_score_with_mortgage = models.IntegerField(null=True)
    indebt_min = models.FloatField(null=True)
    delinquent_mortgage = models.BooleanField(default=False)
    active_bunkruptcy = models.BooleanField(default=False)
    debt_in_income_min = models.FloatField(null=True)
    debt_in_income_max = models.FloatField(null=True)
    last_credit = models.DateTimeField(null=True)

    # affordability
    confidence_factor = models.FloatField(null=True)
    indicator_red = models.BooleanField(default=False)

    def extract(self):
        data = CallCreditConvertor().convert(self.data)
        for key, value in data.items():
            setattr(self, key, value)
        self.save()


class Setting(models.Model):
    name = models.CharField(max_length=50)
    is_active = models.BooleanField(default=False)
    updated_at = models.DateTimeField(auto_now=True)

    age_max = models.IntegerField(default=64, blank=True)
    age_min = models.IntegerField(default=25, blank=True)
    employment_status = models.PositiveSmallIntegerField(
        choices=EMPLOYMENT_CHOICES, default=1, blank=True)
    income_min = models.FloatField(default=1000, blank=True)
    loan_amount_min = models.FloatField(default=500, blank=True)
    loan_amount_max = models.FloatField(default=2000, blank=True)
    employer = models.BooleanField(default=True, blank=True)
    occupation = models.BooleanField(default=True, blank=True)
    postcode = models.BooleanField(default=True, blank=True)

    def __str__(self):
        return f'{self.name}'

    @classmethod
    def get_setting(cls):
        instances = cls.objects.filter(is_active=True).order_by('id')
        if len(instances):
            return instances[0]
        return cls.objects.create(is_active=True)


class History(models.Model):
    applicant = models.ForeignKey(Applicant, related_name='history', on_delete=models.CASCADE)
    call_credit = models.ForeignKey(
        CallCredit,
        null=True,
        related_name='history',
        on_delete=models.CASCADE
    )
    result = models.PositiveSmallIntegerField(choices=RESULT_CHOICES)
    data = JSONField()
    created_at = models.DateTimeField(auto_now_add=True)

    @classmethod
    def add(cls, applicant, result, call_credit=None, data={}):
        return cls.objects.create(
            applicant=applicant,
            result=result,
            call_credit=call_credit,
            data=data
        )
