# -*- coding: utf-8 -*-
# Generated by Django 1.10.7 on 2017-09-28 04:43
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0011_auto_20170928_0436'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='article',
            name='created_date',
        ),
        migrations.RemoveField(
            model_name='article',
            name='published_date',
        ),
        migrations.AddField(
            model_name='article',
            name='publish',
            field=models.DateField(default=datetime.datetime(2017, 9, 28, 4, 43, 40, 517132, tzinfo=utc)),
            preserve_default=False,
        ),
    ]
