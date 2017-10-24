# -*- coding: utf-8 -*-
# Generated by Django 1.10.7 on 2017-10-24 02:46
from __future__ import unicode_literals

from django.db import migrations
import easy_thumbnails.fields
import hosts.models


class Migration(migrations.Migration):

    dependencies = [
        ('hosts', '0026_auto_20171024_0243'),
    ]

    operations = [
        migrations.AlterField(
            model_name='uploadstudyoffer',
            name='image',
            field=easy_thumbnails.fields.ThumbnailerImageField(upload_to=hosts.models.get_image_path),
        ),
    ]