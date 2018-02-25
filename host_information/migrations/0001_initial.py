# -*- coding: utf-8 -*-
# Generated by Django 1.10.7 on 2018-02-25 20:55
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='EntertainmentActivities',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('description', models.CharField(blank=True, max_length=255, null=True)),
            ],
            options={
                'verbose_name': 'Actividades de Entretenimiento',
                'verbose_name_plural': 'Actividades de Entretenimiento',
            },
        ),
        migrations.CreateModel(
            name='FeaturesAmenities',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('description', models.CharField(blank=True, max_length=255, null=True)),
            ],
            options={
                'verbose_name': 'Comodidades destacadas',
                'verbose_name_plural': 'Comodidades destacadas',
            },
        ),
        migrations.CreateModel(
            name='OfferedServices',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('description', models.CharField(blank=True, max_length=255, null=True)),
            ],
            options={
                'verbose_name': 'Servicios ofrecidos',
                'verbose_name_plural': 'Servicios ofrecidos',
            },
        ),
        migrations.CreateModel(
            name='RoomInformation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('description', models.CharField(blank=True, max_length=255, null=True)),
            ],
            options={
                'verbose_name': 'Características del cuarto',
                'verbose_name_plural': 'Características del cuarto',
            },
        ),
        migrations.CreateModel(
            name='SpeakLanguages',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
            ],
            options={
                'verbose_name': 'Idiomas',
                'verbose_name_plural': 'Idiomas',
            },
        ),
    ]
