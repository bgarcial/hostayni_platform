# -*- coding: utf-8 -*-
# Generated by Django 1.10.7 on 2018-04-21 11:15
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_auto_20180419_0521'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='full_name',
            field=models.CharField(max_length=60, verbose_name='full name'),
        ),
    ]