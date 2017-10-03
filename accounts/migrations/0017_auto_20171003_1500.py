# -*- coding: utf-8 -*-
# Generated by Django 1.10.7 on 2017-10-03 15:00
from __future__ import unicode_literals

from django.db import migrations, models
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0016_auto_20171003_1427'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='address',
            field=models.CharField(blank=True, default=1, max_length=128, verbose_name='Dirección'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='user',
            name='biography',
            field=models.TextField(blank=True, default=1, verbose_name='Biografía'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='user',
            name='city_current_residence',
            field=models.CharField(blank=True, default=1, max_length=255, verbose_name='Ciudad de residencia'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='user',
            name='description',
            field=models.TextField(blank=True, default=1, verbose_name='Descripción de la empresa'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='user',
            name='enterprise_name',
            field=models.CharField(blank=True, default=1, max_length=100, verbose_name='Nombre de la organización'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='user',
            name='phone_number',
            field=phonenumber_field.modelfields.PhoneNumberField(blank=True, default=1, help_text='Por favor use el siguiente formato: <em>+Country Code-Number</em>.', max_length=128, verbose_name='Número de contacto'),
            preserve_default=False,
        ),
    ]
