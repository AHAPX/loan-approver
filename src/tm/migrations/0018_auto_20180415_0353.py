# Generated by Django 2.0 on 2018-04-15 03:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tm', '0017_auto_20180415_0337'),
    ]

    operations = [
        migrations.RenameField(
            model_name='setting',
            old_name='dti_ratio',
            new_name='dti_margin',
        ),
        migrations.AlterField(
            model_name='introducer',
            name='auth_code',
            field=models.CharField(default='n6L4nmISPcSlvdzvf8Tep5QZ2ETwe2vUWUfZMlu1fuao2dZpOJjiuCO58VECrvut', max_length=64),
        ),
    ]
