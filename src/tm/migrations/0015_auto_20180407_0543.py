# Generated by Django 2.0 on 2018-04-07 05:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tm', '0014_auto_20180327_1045'),
    ]

    operations = [
        migrations.AlterField(
            model_name='introducer',
            name='auth_code',
            field=models.CharField(default='o79rv2KfRFPoY0nXXTUl8CIZ6KexXuiSyYkvz1SAoa27pbAzZX6LdHSehVojv1Sc', max_length=64),
        ),
        migrations.AlterField(
            model_name='introducer',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='introducer',
            name='name',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]