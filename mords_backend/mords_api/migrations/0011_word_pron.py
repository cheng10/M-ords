# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-12-09 19:44
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mords_api', '0010_auto_20161209_0149'),
    ]

    operations = [
        migrations.AddField(
            model_name='word',
            name='pron',
            field=models.CharField(default='', help_text='pronunciation of the word', max_length=200),
        ),
    ]