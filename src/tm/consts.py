from enum import Enum


class TEMPLATES(Enum):
    LOANPACK = 1
    CANCEL_FORM = 2
    REFUND = 3
    LOAN_AGREEMENT = 4
    EXPLANATIONS = 5
    SECCI = 6
    FAIL_SCORE = 7
    BANK_STATEMENT = 8
    VERIFY_MOBILE = 9
    VERIFY_LANDLINE = 10
    SEND_EXPAND_SECCI = 11
    MAX_PROD_ASSIGNED = 12
    SMS_MAX_PROD_ASSIGNED = 13
    THANK_YOU = 14
    AGREEMENT_UNSIGNED = 15
    AGREEMENT_SIGNED = 16
    WHEN_DECLINED = 17
    WHEN_FUNDED = 18
    WHEN_SIGNED_OFF = 19


class STATES(Enum):
    BEGIN = 1


TEMPLATES_CHOICES = (
    (TEMPLATES.LOANPACK, 'Loan Pack'),
    (TEMPLATES.CANCEL_FORM, 'Cancellation Form'),
    (TEMPLATES.REFUND, 'Refund Confirmation'),
    (TEMPLATES.LOAN_AGREEMENT, 'Loan Agreement'),
    (TEMPLATES.EXPLANATIONS, 'Explanations'),
    (TEMPLATES.SECCI, 'SECCI'),
    (TEMPLATES.FAIL_SCORE, 'Failed Credit Score'),
    (TEMPLATES.BANK_STATEMENT, 'Bank Statement Needed'),
    (TEMPLATES.VERIFY_MOBILE, 'Verify Mobile PIN'),
    (TEMPLATES.VERIFY_LANDLINE, 'Verify Landline PIN'),
    (TEMPLATES.SEND_EXPAND_SECCI, 'Send explantion and SECCI'),
    (TEMPLATES.MAX_PROD_ASSIGNED, 'EMail: Product Assigned'),
    (TEMPLATES.SMS_MAX_PROD_ASSIGNED, 'SMS: Product Assigned'),
    (TEMPLATES.THANK_YOU, 'Thank You Page'),
    (TEMPLATES.AGREEMENT_UNSIGNED, 'SMS: Agreement unsigned for 10 mins'),
    (TEMPLATES.AGREEMENT_SIGNED, 'SMS: 10 mins after agreement signed'),
    (TEMPLATES.WHEN_DECLINED, 'SMS: When declined by underwriter'),
    (TEMPLATES.WHEN_FUNDED, 'SMS: When funded'),
    (TEMPLATES.WHEN_SIGNED_OFF, 'SMS: When signed off'),
)

SEX_CHOICES = (
    ('M', 'Male'),
    ('F', 'Female'),
)

TITLE_CHOICES = (
    (1, 'Mr'),
    (2, 'Mrs'),
    (3, 'Miss'),
    (4, 'Ms'),
    (5, 'Dr'),
)

MARITAL_CHOICES = (
    (1, 'Married'),
    (2, 'Single'),
    (3, 'Divorced'),
    (4, 'Separated'),
    (5, 'Widowed'),
    (6, 'CommonLaw'),
)

RESIDENTIAL_CHOICES = (
    (1, 'Home owner'),
    (2, 'Living with parents'),
    (3, 'Private tenant'),
    (4, 'Council tenant housing association'),
)

LIVE_WITH_CHOICES = (
    (1, 'I live alone'),
    (2, 'I am single parent'),
    (3, 'I live with my partner'),
    (4, 'I live in a house share'),
    (5, 'I live with parents'),
)

EMPLOYMENT_CHOICES = (
    (1, 'Full time'),
    (2, 'Part time'),
    (3, 'Self employed'),
    (4, 'Unemployed'),
    (5, 'Home maker'),
    (6, 'Retired'),
)

PAYMENT_CHOICES = (
    (1, 'Straight to bank'),
    (2, 'Cheque'),
    (3, 'Cash in hand'),
)

PAY_FREQUENCY_CHOICES = (
    (1, 'Monthly'),
    (2, 'Weekly'),
    (3, 'Fortnightly'),
    (4, 'FourWeekly'),
)


SETTING_TYPE_CHOICES = (
    ('str', 'str'),
    ('int', 'int'),
    ('float', 'float'),
    ('bool', 'bool'),
)
