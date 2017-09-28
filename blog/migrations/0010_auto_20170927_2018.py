# -*- coding: utf-8 -*-
# Generated by Django 1.10.7 on 2017-09-27 20:18
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0009_auto_20170927_2013'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='height_field',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='article',
            name='width_field',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='article',
            name='image',
            field=models.ImageField(height_field='height_field', upload_to='', width_field='width_field'),
        ),
    ]
