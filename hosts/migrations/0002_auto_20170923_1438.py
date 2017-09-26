# -*- coding: utf-8 -*-
# Generated by Django 1.10.7 on 2017-09-23 14:38
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django_countries.fields
import taggit.managers


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('taggit', '0002_auto_20150616_2121'),
        ('hosts', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='StudiesOffert',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ad_title', models.CharField(max_length=255, verbose_name='Título de la oferta')),
                ('country', django_countries.fields.CountryField(max_length=2, verbose_name='País')),
                ('city', models.CharField(max_length=255, verbose_name='Ciudad')),
                ('address', models.CharField(max_length=255, verbose_name='Dirección')),
                ('latitude', models.CharField(blank=True, max_length=255, null=True, verbose_name='latitude')),
                ('longitude', models.CharField(blank=True, max_length=255, null=True, verbose_name='longitude')),
                ('institute_character', models.CharField(choices=[('Private', 'Privada'), ('Public', 'Pública'), ('Private - Public', 'Privada - Pública')], max_length=20, verbose_name='Caracter de la institución')),
                ('maximum_quota', models.PositiveSmallIntegerField(verbose_name='Cupo máximo de estudiantes')),
                ('studies_type_offered', models.CharField(choices=[('Continuing Education studies', 'Estudios de educación contínua'), ('Technique', 'Tecnología'), ('Technology', 'Técnica'), ('Professional', 'Profesional'), ('Specialization', 'Especialización'), ('Master', 'Maestría'), ('Doctorate', 'Doctorado'), ('Academic_Mobility', 'Movilidad académica')], max_length=255, verbose_name='Tipo de estudios ofertados')),
                ('academic_mobility_programs', models.CharField(choices=[('Academic Semester', 'Semestre académico'), ('Research', 'Investigación'), ('Rotations or Practices', 'Rotaciones o prácticas'), ('Summer School', 'Escuela de verano')], help_text='Available student academic mobility programs', max_length=255, verbose_name='Academic mobility programs')),
                ('duration', models.CharField(max_length=255, verbose_name='Duración')),
                ('modality', models.CharField(choices=[('Virtual', 'Virtual'), ('On_site', 'Presencial')], max_length=20, verbose_name='Modalidad')),
                ('studies_value', models.CharField(max_length=128, verbose_name='Price')),
                ('additional_description', models.TextField()),
                ('photo', models.ImageField(blank=True, null=True, upload_to='study-host-offert-photos', verbose_name='Photography')),
                ('pub_date', models.DateTimeField(auto_now=True)),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('knowledge_topics', taggit.managers.TaggableManager(help_text='Una lista de temáticas separada por comas.', through='taggit.TaggedItem', to='taggit.Tag', verbose_name='Tópicos de conocimiento')),
            ],
        ),
        migrations.CreateModel(
            name='StudiesTypeOffered',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('description', models.CharField(blank=True, max_length=255, null=True)),
            ],
            options={
                'verbose_name': 'Tipo de estudio ofertado',
                'verbose_name_plural': 'Tipo de estudios ofertados',
            },
        ),
        migrations.AlterField(
            model_name='lodgingoffer',
            name='ad_title',
            field=models.CharField(max_length=255, verbose_name='Título de la oferta'),
        ),
    ]