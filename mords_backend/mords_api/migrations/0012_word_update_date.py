# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-12-09 20:22
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mords_api', '0011_word_pron'),
    ]

    operations = [
        migrations.AddField(
            model_name='word',
            name='update_date',
            field=models.DateField(null=True),
        ),
    ]
