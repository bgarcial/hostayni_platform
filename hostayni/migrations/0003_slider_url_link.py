# -*- coding: utf-8 -*-
# Generated by Django 1.10.7 on 2018-02-13 08:34
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hostayni', '0002_auto_20180213_0805'),
    ]

    operations = [
        migrations.AddField(
            model_name='slider',
            name='url_link',
            field=models.CharField(blank=True, max_length=250, null=True),
        ),
    ]
