# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-12-09 20:55
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mords_api', '0017_auto_20161209_1344'),
    ]

    operations = [
        migrations.AddField(
            model_name='word',
            name='uk_pho',
            field=models.CharField(default='', max_length=200),
        ),
        migrations.AddField(
            model_name='word',
            name='us_pho',
            field=models.CharField(default='', max_length=200),
        ),
    ]