# Generated by Django 2.1.7 on 2019-03-17 18:01

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainpage', '0003_auto_20190317_2323'),
    ]

    operations = [
        migrations.AlterField(
            model_name='entry',
            name='end_date',
            field=models.DateTimeField(),
        ),
        migrations.AlterField(
            model_name='entry',
            name='start_date',
            field=models.DateTimeField(default=datetime.datetime(2019, 3, 17, 23, 31, 11, 920704)),
        ),
    ]
