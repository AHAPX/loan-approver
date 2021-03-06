# Generated by Django 2.0 on 2018-03-27 10:45

from django.db import migrations, models
import tm.helpers


class Migration(migrations.Migration):

    dependencies = [
        ('tm', '0013_applicant_reference_number'),
    ]

    operations = [
        migrations.AddField(
            model_name='applicant',
            name='is_signed',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='applicant',
            name='reference_number',
            field=models.IntegerField(default=tm.helpers.gen_reference_num, null=True),
        ),
        migrations.AlterField(
            model_name='template',
            name='usefor',
            field=models.IntegerField(choices=[(1, 'Loan Pack'), (2, 'Cancellation Form'), (3, 'Refund Confirmation'), (4, 'Loan Agreement'), (5, 'Explanations'), (6, 'SECCI'), (7, 'Failed Credit Score'), (8, 'Bank Statement Needed'), (9, 'Verify Mobile PIN'), (10, 'Verify Landline PIN'), (11, 'Send explantion and SECCI'), (12, 'EMail: Product Assigned'), (13, 'SMS: Product Assigned'), (14, 'Thank You Page'), (15, 'SMS: Agreement unsigned for 10 mins'), (16, 'SMS: 10 mins after agreement signed'), (17, 'SMS: When declined by underwriter'), (18, 'SMS: When funded'), (19, 'SMS: When signed off'), (20, 'Footer: customer pages')], unique=True),
        ),
    ]
