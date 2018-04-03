# -*- coding: utf-8 -*-
# Generated by Django 1.10.7 on 2018-03-27 12:20
from __future__ import unicode_literals

import carousel_offers.models
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('carousel_offers', '0002_entrepreneurshipoffercarousel'),
    ]

    operations = [
        migrations.CreateModel(
            name='DailyLifeOfferCarousel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=120, verbose_name='Ingrese el nombre de quien pauta')),
                ('slug', models.SlugField(blank=True, max_length=100)),
                ('image', models.ImageField(upload_to=carousel_offers.models.daily_life_slider_upload, verbose_name='Imagen a aparecer en el carrusel')),
                ('order', models.IntegerField(default=0, help_text='Ingrese un numero', verbose_name='Ingrese el orden en que desea que aparezca la imagen')),
                ('url_link', models.CharField(blank=True, help_text='Opcional', max_length=250, null=True, verbose_name='Ingrese un enlace promocional')),
                ('header_text', models.CharField(blank=True, help_text='Opcional', max_length=120, null=True, verbose_name='Ingrese un encabezado para el banner')),
                ('text', models.CharField(blank=True, help_text='Opcional', max_length=120, null=True, verbose_name='Ingrese un caption para el banner')),
                ('active', models.BooleanField(default=False, help_text='Indica si el anuncio estara activo o no en la pagina de busquedas de ofertas de vida diaria')),
                ('featured', models.BooleanField(default=False)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('start_date', models.DateField(blank=True, help_text='Indica desde que fecha el anuncio empezara a aparecer en la pagina de busquedas de ofertas de vida diaria', null=True, verbose_name='Fecha de inicio del anuncio')),
                ('end_date', models.DateField(blank=True, help_text='Indica hasta que fecha el anuncio estara en la pagina de busquedas de emprendimiento', null=True, verbose_name='Fecha de finalizacion del anuncio')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['order', '-start_date', '-end_date'],
            },
        ),
        migrations.AlterField(
            model_name='entrepreneurshipoffercarousel',
            name='active',
            field=models.BooleanField(default=False, help_text='Indica si el anuncio estara activo o no en la pagina de busquedas de emprendimiento'),
        ),
        migrations.AlterField(
            model_name='entrepreneurshipoffercarousel',
            name='end_date',
            field=models.DateField(blank=True, help_text='Indica hasta que fecha el anuncio estara en la pagina de busquedas de emprendimiento', null=True, verbose_name='Fecha de finalizacion del anuncio'),
        ),
        migrations.AlterField(
            model_name='entrepreneurshipoffercarousel',
            name='start_date',
            field=models.DateField(blank=True, help_text='Indica desde que fecha el anuncio empezara a aparecer en la pagina de busquedas de emprendimiento', null=True, verbose_name='Fecha de inicio del anuncio'),
        ),
    ]
