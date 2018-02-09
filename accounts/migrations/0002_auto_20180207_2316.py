# -*- coding: utf-8 -*-
# Generated by Django 1.10.7 on 2018-02-07 23:16
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='executiveprofile',
            name='complete_studies_school',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Institución en donde terminó sus estudios anteriores'),
        ),
        migrations.AlterField(
            model_name='executiveprofile',
            name='educational_titles',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Títulos educativos'),
        ),
        migrations.AlterField(
            model_name='executiveprofile',
            name='enterprise_name',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Compañía con la cual esta vinculado'),
        ),
        migrations.AlterField(
            model_name='executiveprofile',
            name='innovation_topics_choice',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Areas de innovación de su elección'),
        ),
        migrations.AlterField(
            model_name='professorprofile',
            name='autorship_publications',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Publications of its authorship'),
        ),
        migrations.AlterField(
            model_name='professorprofile',
            name='complete_studies_school',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Institución en donde terminó sus estudios anteriores'),
        ),
        migrations.AlterField(
            model_name='professorprofile',
            name='current_education_school',
            field=models.CharField(blank=True, max_length=128, null=True, verbose_name='Institución educativa en la cual está vinculado en su actual lugar residencia'),
        ),
        migrations.AlterField(
            model_name='professorprofile',
            name='educational_titles',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Títulos educativos'),
        ),
        migrations.AlterField(
            model_name='professorprofile',
            name='knowledge_topics_choice',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Areas de conocimiento de su elección'),
        ),
        migrations.AlterField(
            model_name='professorprofile',
            name='occupation',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='professorprofile',
            name='origin_education_school',
            field=models.CharField(blank=True, max_length=128, null=True, verbose_name='Institución de educación de origen'),
        ),
        migrations.AlterField(
            model_name='professorprofile',
            name='research_groups',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Grupos de Investigación a los que pertenece'),
        ),
        migrations.AlterField(
            model_name='studentprofile',
            name='complete_studies_school',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Institución en donde completó sus estudios anteriores'),
        ),
        migrations.AlterField(
            model_name='studentprofile',
            name='educational_titles',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Titulos Educativos'),
        ),
        migrations.AlterField(
            model_name='studentprofile',
            name='extra_occupation',
            field=models.CharField(blank=True, max_length=128, null=True, verbose_name='Ocupación Extra'),
        ),
        migrations.AlterField(
            model_name='studentprofile',
            name='knowledge_topics_choice',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Áreas de conocimiento de su elección'),
        ),
        migrations.AlterField(
            model_name='studentprofile',
            name='origin_education_school',
            field=models.CharField(blank=True, max_length=128, null=True, verbose_name='Institución de educación de origen'),
        ),
    ]