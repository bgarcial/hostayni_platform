# -*- coding: utf-8 -*-
# Generated by Django 1.10.7 on 2017-10-25 14:46
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('hosts', '0033_remove_studiesoffert_photo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lodgingofferimage',
            name='lodging_offer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='lodgingofferimage', to='hosts.LodgingOffer'),
        ),
    ]
