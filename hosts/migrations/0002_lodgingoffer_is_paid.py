# -*- coding: utf-8 -*-
# Generated by Django 1.10.7 on 2018-01-20 21:09
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hosts', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='lodgingoffer',
            name='is_paid',
            field=models.BooleanField(default=False, verbose_name='Oferta promovida'),
        ),
    ]