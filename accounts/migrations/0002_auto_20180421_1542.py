# -*- coding: utf-8 -*-
# Generated by Django 1.10.7 on 2018-04-21 15:42
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='user',
            options={'verbose_name': 'user', 'verbose_name_plural': 'Usuarios en la plataforma'},
        ),
    ]
