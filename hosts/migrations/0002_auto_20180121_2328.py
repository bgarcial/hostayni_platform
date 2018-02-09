# -*- coding: utf-8 -*-
# Generated by Django 1.10.7 on 2018-01-21 23:28
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hosts', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lodgingoffer',
            name='stars',
            field=models.CharField(blank=True, choices=[(' ', ' '), ('1 estrella', '1 estrella'), ('2 estrellas', '2 estrellas'), ('3 estrellas', '3 estrellas'), ('4 estrellas', '4 estrellas'), ('5 estrellas', '5 estrellas')], max_length=255, null=True, verbose_name='Número de estrellas'),
        ),
    ]