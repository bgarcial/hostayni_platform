# -*- coding: utf-8 -*-
# Generated by Django 1.10.7 on 2018-02-07 23:23
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_auto_20180207_2319'),
    ]

    operations = [
        migrations.AlterField(
            model_name='professorprofile',
            name='autorship_publications',
            field=models.CharField(blank=True, default=1, max_length=255, verbose_name='Publications of its authorship'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='professorprofile',
            name='research_groups',
            field=models.CharField(blank=True, default=1, max_length=255, verbose_name='Grupos de Investigación a los que pertenece'),
            preserve_default=False,
        ),
    ]