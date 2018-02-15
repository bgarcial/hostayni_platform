# -*- coding: utf-8 -*-
# Generated by Django 1.10.7 on 2018-02-15 13:05
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hosts', '0002_auto_20180121_2328'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lodgingoffer',
            name='number_guest_room_type',
            field=models.CharField(choices=[('Para 1 huésped', 'Para 1 huésped'), ('Para 2 huéspedes', 'Para 2 huéspedes'), ('Para 3 huéspede', 'Para 3 huéspedes'), ('Para 4 huéspedes', 'Para 4 huéspedes'), ('Para 5 huéspedes', 'Para 5 huéspedes'), ('Para 6 huéspedes', 'Para 6 huéspedes'), ('Para 7 huéspedes', 'Para 7 huéspedes'), ('Para 8 huéspedes', 'Para 8 huéspedes')], max_length=255, verbose_name='Número de huéspedes en habitación'),
        ),
    ]
