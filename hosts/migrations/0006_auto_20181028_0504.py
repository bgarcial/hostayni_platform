# -*- coding: utf-8 -*-
# Generated by Django 1.10.7 on 2018-10-28 05:04
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hosts', '0005_auto_20181028_0436'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='lodgingoffer',
            name='bed_type',
        ),
        migrations.RemoveField(
            model_name='lodgingoffer',
            name='lodging_offer_type',
        ),
        migrations.RemoveField(
            model_name='lodgingoffer',
            name='lodging_offer_type_org',
        ),
        migrations.RemoveField(
            model_name='lodgingoffer',
            name='stars',
        ),
    ]
