# -*- coding: utf-8 -*-
# Generated by Django 1.10.7 on 2017-10-03 13:56
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hosts', '0007_auto_20171002_2057'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lodgingoffer',
            name='check_in',
            field=models.DateField(blank=True, help_text='Por favor use el formato: <em>DD/MM/YYYY</em>.', null=True, verbose_name='Check In'),
        ),
        migrations.AlterField(
            model_name='lodgingoffer',
            name='check_out',
            field=models.DateField(blank=True, help_text='Por favor use el formato: <em>DD/MM/YYYY</em>.', null=True, verbose_name='Check Out'),
        ),
    ]