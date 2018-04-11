# -*- coding: utf-8 -*-
# Generated by Django 1.10.7 on 2018-04-07 22:18
from __future__ import unicode_literals

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('entrepreneurship', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='entrepreneurshipoffer',
            name='additional_description',
            field=models.TextField(blank=True, null=True, verbose_name='Descripción adicional'),
        ),
        migrations.AlterField(
            model_name='entrepreneurshipoffer',
            name='url',
            field=models.TextField(blank=True, help_text='Para mayor información referencie una dirección o enlace web', null=True, validators=[django.core.validators.URLValidator()], verbose_name='Dirección de enlace'),
        ),
    ]
