# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-12-09 20:29
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('mords_api', '0013_auto_20161209_1325'),
    ]

    operations = [
        migrations.AlterField(
            model_name='word',
            name='update_date',
            field=models.DateField(default=datetime.datetime(2016, 12, 9, 20, 29, 4, 985536, tzinfo=utc)),
        ),
    ]
