# -*- coding: utf-8 -*-
# Generated by Django 1.10.7 on 2018-10-26 18:56
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0007_auto_20181026_1801'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='user_type',
        ),
    ]