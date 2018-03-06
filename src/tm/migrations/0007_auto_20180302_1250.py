# Generated by Django 2.0 on 2018-03-02 12:50

import django.contrib.postgres.fields.jsonb
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tm', '0006_auto_20180227_0511'),
    ]

    operations = [
        migrations.RenameField(
            model_name='callcredit',
            old_name='indebt_min',
            new_name='indebt',
        ),
        migrations.RemoveField(
            model_name='callcredit',
            name='credit_score_with_mortgage',
        ),
        migrations.RemoveField(
            model_name='callcredit',
            name='debt_in_income_max',
        ),
        migrations.RemoveField(
            model_name='callcredit',
            name='debt_in_income_min',
        ),
        migrations.RemoveField(
            model_name='callcredit',
            name='delinquent_mortgage',
        ),
        migrations.RemoveField(
            model_name='callcredit',
            name='last_credit',
        ),
        migrations.AddField(
            model_name='callcredit',
            name='accs',
            field=django.contrib.postgres.fields.jsonb.JSONField(null=True),
        ),
        migrations.AddField(
            model_name='setting',
            name='acc_for_years',
            field=models.IntegerField(blank=True, default=3),
        ),
        migrations.AddField(
            model_name='setting',
            name='active_bunkruptcy',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='setting',
            name='credit_score_min',
            field=models.IntegerField(blank=True, default=0),
        ),
        migrations.AddField(
            model_name='setting',
            name='indebt_min',
            field=models.FloatField(blank=True, default=0),
        ),
    ]