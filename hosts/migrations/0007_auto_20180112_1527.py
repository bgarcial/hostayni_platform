# -*- coding: utf-8 -*-
# Generated by Django 1.10.7 on 2018-01-12 15:27
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import hosts.models


class Migration(migrations.Migration):

    dependencies = [
        ('hosts', '0006_auto_20180112_1506'),
    ]

    operations = [
        migrations.CreateModel(
            name='StudyOfferImage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to=hosts.models.get_image_path, verbose_name='Seleccionar imagen')),
                ('study_offer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='uploadsstudyoffer', to='hosts.StudiesOffert')),
            ],
        ),
        migrations.RemoveField(
            model_name='uploadstudyoffer',
            name='study_offer',
        ),
        migrations.DeleteModel(
            name='UploadStudyOffer',
        ),
    ]
