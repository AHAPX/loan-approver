# Generated by Django 2.0 on 2018-04-15 03:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tm', '0016_auto_20180409_0936'),
    ]

    operations = [
        migrations.AddField(
            model_name='setting',
            name='dti_ratio',
            field=models.FloatField(blank=True, default=0),
        ),
        migrations.AlterField(
            model_name='introducer',
            name='auth_code',
            field=models.CharField(default='UrxSW0pm9e952qm2tCDrXc11zba8vqzYdkYSPI0zc7Tit59jVO2ye2fWj0v1Ukw4', max_length=64),
        ),
    ]