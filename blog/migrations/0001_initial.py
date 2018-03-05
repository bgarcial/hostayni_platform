# -*- coding: utf-8 -*-
# Generated by Django 1.10.7 on 2018-03-05 09:49
from __future__ import unicode_literals

import blog.models
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Article',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=120)),
                ('slug', models.SlugField(blank=True, max_length=100)),
                ('content', models.TextField(verbose_name='Contenido')),
                ('draft', models.BooleanField(default=False, help_text='Si seleccionas esta  opción tu artículo no será publicado por el momento', verbose_name='Borrador')),
                ('publish', models.DateField()),
                ('image', models.ImageField(height_field='height_field', help_text='El tamaño de la imagen debe ser de 1080 por 920', upload_to=blog.models.upload_location, verbose_name='Imagen', width_field='width_field')),
                ('height_field', models.IntegerField(default=0)),
                ('width_field', models.IntegerField(default=0)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-timestamp', '-updated'],
            },
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50, verbose_name='Titulo')),
                ('description', models.TextField(verbose_name='Descripción')),
            ],
        ),
        migrations.AddField(
            model_name='article',
            name='category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='blog.Category', verbose_name='Categoría'),
        ),
    ]
