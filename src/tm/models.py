from django.db import models

from .consts import (
    STATES, TEMPLATES_CHOICES, SEX_CHOICES, TITLE_CHOICES, MARITAL_CHOICES,
    RESIDENTIAL_CHOICES, EMPLOYMENT_CHOICES, PAYMENT_CHOICES,
    PAY_FREQUENCY_CHOICES,
)


class Introducer(models.Model):
    auth_code = models.CharField(max_length=64, null=True, blank=True)
    ip = models.TextField(null=True, blank=True)
    netmask = models.IntegerField(null=True, blank=True, default=32)
    company_name = models.CharField(max_length=100)
    address = models.CharField(max_length=255, null=True, blank=True)
    website = models.URLField(max_length=100, null=True, blank=True)
    phonenumber = models.CharField(max_length=20, null=True, blank=True)
    is_active = models.BooleanField(default=False)


class Template(models.Model):
    name = models.CharField(max_length=100)
    text = models.TextField()
    usefor = models.IntegerField(choices=TEMPLATES_CHOICES)


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


class Applicant(models.Model):
    introducer = models.ForeignKey(Introducer, related_name='applicants', on_delete=models.CASCADE)

    loan_amount = models.DecimalField(decimal_places=2, max_digits=12)
    loan_term = models.PositiveSmallIntegerField(null=True, blank=True)
    loan_purpose = models.TextField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    state = models.IntegerField(default=STATES.BEGIN)

    sex = models.CharField(max_length=1, choices=SEX_CHOICES)
    title = models.PositiveSmallIntegerField(choices=TITLE_CHOICES)

    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    date_of_birth = models.DateField()
    phone_landline = models.CharField(max_length=12)
    phone_mobile = models.CharField(max_length=12, null=False, blank=False)
    email = models.EmailField()

    marital_status = models.PositiveSmallIntegerField(choices=MARITAL_CHOICES, null=True, blank=True)
    adults = models.PositiveSmallIntegerField(null=True, blank=True)
    children = models.PositiveSmallIntegerField(default=0)
    cars = models.PositiveSmallIntegerField(default=0)

    partner_in_come = models.DecimalField(null=True, blank=True, decimal_places=2, max_digits=12)
    partner_contrib = models.DecimalField(null=True, blank=True, decimal_places=2, max_digits=12)
    childcare_costs = models.DecimalField(null=True, blank=True, decimal_places=2, max_digits=12)

    residential_status = models.PositiveSmallIntegerField(choices=RESIDENTIAL_CHOICES)

    # current address
    addr_flat = models.CharField(max_length=10, null=True, blank=True)
    addr_house = models.CharField(max_length=10, null=True, blank=True)
    addr_city = models.CharField(max_length=50, null=True, blank=True)
    addr_county = models.CharField(max_length=50, null=True, blank=True)
    addr_postcode = models.CharField(max_length=8, null=True, blank=True)
    addr_years = models.PositiveSmallIntegerField(null=True, blank=True)
    addr_months = models.PositiveSmallIntegerField(null=True, blank=True)

    # previous address
    addr_flat2 = models.CharField(max_length=10, null=True, blank=True)
    addr_house2 = models.CharField(max_length=10, null=True, blank=True)
    addr_city2 = models.CharField(max_length=50, null=True, blank=True)
    addr_county2 = models.CharField(max_length=50, null=True, blank=True)
    addr_postcode2 = models.CharField(max_length=8, null=True, blank=True)
    addr_years2 = models.PositiveSmallIntegerField(null=True, blank=True)
    addr_months2 = models.PositiveSmallIntegerField(null=True, blank=True)

    # employment details
    employment_status = models.PositiveSmallIntegerField(choices=EMPLOYMENT_CHOICES)
    employer_name = models.CharField(max_length=100, null=True, blank=True)
    employed_years = models.PositiveSmallIntegerField(null=True, blank=True)
    employed_months = models.PositiveSmallIntegerField(null=True, blank=True)
    employer_address = models.CharField(max_length=100, null=True, blank=True)
    employer_city = models.CharField(max_length=50, null=True, blank=True)
    employer_county = models.CharField(max_length=50, null=True, blank=True)
    employer_postcode = models.CharField(max_length=8, null=True, blank=True)
    employer_phone = models.CharField(max_length=20, null=True, blank=True)
    job_title = models.CharField(max_length=50, null=True, blank=True)
    income = models.DecimalField(null=True, blank=True, decimal_places=2, max_digits=12)
    hours_per_week = models.PositiveSmallIntegerField(null=True, blank=True)

    payment_method = models.PositiveSmallIntegerField(choices=PAYMENT_CHOICES, null=True, blank=True)

    # financials
    rent_mortgage = models.DecimalField(null=True, blank=True, decimal_places=2, max_digits=12)
    nin = models.CharField(max_length=12, null=True, blank=True)

    # bank details
    bank_account_number = models.CharField(max_length=20, null=True, blank=True)
    bank_sort_code = models.CharField(max_length=6, null=True, blank=True)

    pay_frequency = models.PositiveSmallIntegerField(choices=PAY_FREQUENCY_CHOICES, null=True, blank=True)
    next_pay_date = models.DateField(null=True, blank=True)

    # callcredit data
    cc_credit_score = models.IntegerField(null=True, blank=True)
    cc_total_balances_active = models.IntegerField(null=True, blank=True)
