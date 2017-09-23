# -*- coding: utf-8 -*-
# Generated by Django 1.10.7 on 2017-09-23 06:31
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_auto_20170922_1634'),
    ]

    operations = [
        migrations.AddField(
            model_name='professorprofile',
            name='autorship_publications',
            field=models.CharField(default=1, max_length=255, verbose_name='Publications of its authorship'),
            preserve_default=False,
        ),
    ]
