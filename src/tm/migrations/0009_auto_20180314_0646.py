# Generated by Django 2.0 on 2018-03-14 06:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tm', '0008_applicant_sms_token'),
    ]

    operations = [
        migrations.RenameField(
            model_name='applicant',
            old_name='sms_token',
            new_name='access_token',
        ),
    ]