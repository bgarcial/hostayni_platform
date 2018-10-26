# -*- coding: utf-8 -*-
# Generated by Django 1.10.7 on 2018-10-26 22:08
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('entrepreneurship', '0002_auto_20180505_1718'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='entrepreneurshipoffer',
            name='contact_name',
        ),
        migrations.RemoveField(
            model_name='entrepreneurshipoffer',
            name='email',
        ),
        migrations.RemoveField(
            model_name='entrepreneurshipoffer',
            name='offer_type',
        ),
        migrations.RemoveField(
            model_name='entrepreneurshipoffer',
            name='phone_number',
        ),
        migrations.RemoveField(
            model_name='entrepreneurshipoffer',
            name='url',
        ),
        migrations.AddField(
            model_name='entrepreneurshipoffer',
            name='discounts',
            field=models.CharField(blank=True, help_text='Precio en pesos colombianos', max_length=128, null=True, verbose_name='Descuento'),
        ),
        migrations.AddField(
            model_name='entrepreneurshipoffer',
            name='status',
            field=models.CharField(choices=[('Cupos disponibles', 'Cupos disponibles'), ('Voluntariados', 'Cupos agotados'), ('Finalizado', 'Finalizado'), ('Cancelado', 'Cancelado')], default=False, max_length=10, verbose_name='Tipo de Usuario'),
        ),
        migrations.AlterField(
            model_name='entrepreneurshipoffer',
            name='date',
            field=models.DateField(blank=True, help_text='Ingresar aquí la fecha del evento o cierre de la convocatoria', null=True, verbose_name='Fecha'),
        ),
    ]
