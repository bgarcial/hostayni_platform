# -*- coding: utf-8 -*-
# Generated by Django 1.10.7 on 2017-09-30 23:57
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0008_auto_20170930_2350'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='bio',
            new_name='biography',
        ),
    ]