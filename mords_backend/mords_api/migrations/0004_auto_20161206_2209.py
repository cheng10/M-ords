# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-12-07 05:09
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mords_api', '0003_auto_20161206_2151'),
    ]

    operations = [
        migrations.RenameField(
            model_name='entry',
            old_name='reporter',
            new_name='book',
        ),
        migrations.AddField(
            model_name='book',
            name='update_date',
            field=models.DateField(null=True),
        ),
    ]
