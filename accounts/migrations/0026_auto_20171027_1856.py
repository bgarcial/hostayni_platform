# -*- coding: utf-8 -*-
# Generated by Django 1.10.7 on 2017-10-27 18:56
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0025_auto_20171013_1551'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='hostinghostprofile',
            name='user',
        ),
        migrations.DeleteModel(
            name='HostingHostProfile',
        ),
    ]
