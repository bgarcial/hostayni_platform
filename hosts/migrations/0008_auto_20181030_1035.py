# -*- coding: utf-8 -*-
# Generated by Django 1.10.7 on 2018-10-30 10:35
from __future__ import unicode_literals

from django.db import migrations, models
import hosts.models


class Migration(migrations.Migration):

    dependencies = [
        ('hosts', '0007_auto_20181028_0652'),
    ]

    operations = [
        migrations.AddField(
            model_name='studiesoffert',
            name='discounts',
            field=models.CharField(default=1, help_text='Descuentos', max_length=128, verbose_name='Precio'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='studiesoffert',
            name='organizers',
            field=models.ImageField(blank=True, help_text='Logos de los organizadores', null=True, upload_to=hosts.models.get_image_supporters_search_path, verbose_name='Organizadores'),
        ),
        migrations.AddField(
            model_name='studiesoffert',
            name='place',
            field=models.CharField(default=1, max_length=255, verbose_name='Lugar'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='studiesoffert',
            name='schedule',
            field=models.CharField(default=1, max_length=255, verbose_name='Horario'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='studiesoffert',
            name='sponsors',
            field=models.ImageField(blank=True, help_text='Logos de los patrocinadores', null=True, upload_to=hosts.models.get_image_supporters_search_path, verbose_name='Patrocinadores'),
        ),
        migrations.AddField(
            model_name='studiesoffert',
            name='status',
            field=models.CharField(choices=[('Cupos disponibles', 'Cupos disponibles'), ('Cupos agotados', 'Cupos agotados'), ('Finalizada', 'Finalizada'), ('Cancelada', 'Cancelada')], default=1, max_length=255, verbose_name='Estado'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='studiesoffert',
            name='support',
            field=models.ImageField(blank=True, help_text='Logos de quien apoya', null=True, upload_to=hosts.models.get_image_supporters_search_path, verbose_name='Apoya'),
        ),
    ]
