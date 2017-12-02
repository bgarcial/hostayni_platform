# -*- coding: utf-8 -*-
# Generated by Django 1.10.7 on 2017-11-26 04:26
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django_countries.fields
import hosts.models
import taggit.managers


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('taggit', '0002_auto_20150616_2121'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('host_information', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='LodgingOffer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ad_title', models.CharField(max_length=255, verbose_name='Título de la oferta')),
                ('slug', models.SlugField(blank=True, max_length=100)),
                ('country', django_countries.fields.CountryField(max_length=2, verbose_name='Pais')),
                ('city', models.CharField(max_length=255, verbose_name='Ciudad')),
                ('address', models.CharField(max_length=255, verbose_name='Dirección')),
                ('latitude', models.CharField(blank=True, max_length=255, null=True, verbose_name='latitude')),
                ('longitude', models.CharField(blank=True, max_length=255, null=True, verbose_name='longitude')),
                ('lodging_offer_type', models.CharField(choices=[('Hotel', 'Hotel'), ('Hostal', 'Hostal'), ('Residencia estudiantil', 'Residencia estudiantil'), ('Acomodación con familia local', 'Acomodación con familia local'), ('Casa o apartamento para compartir con otros huéspedes', 'Casa o apartamento para compartir con otros huéspedes'), ('Casa o apartamento privado', 'Casa o apartamento privado')], max_length=255, verbose_name='Tipo de oferta de alojamiento')),
                ('stars', models.CharField(choices=[('1 estrella', '1 estrella'), ('2 estrellas', '2 estrellas'), ('3 estrellas', '3 estrellas'), ('4 estrellas', '4 estrellas'), ('5 estrellas', '5 estrellas')], max_length=255, verbose_name='Número de estrellas')),
                ('check_in', models.DateField(blank=True, help_text='Por favor use el formato: <em>YYYY-MM-DD</em>.', null=True, verbose_name='Check In')),
                ('check_out', models.DateField(blank=True, help_text='Por favor use el formato: <em>YYYY-MM-DD</em>.', null=True, verbose_name='Check Out')),
                ('room_type_offered', models.CharField(choices=[('Toda la propiedad', 'Toda la propiedad'), ('Habitación privada', 'Habitación privada'), ('Habitación compartida', 'Habitación compartida')], max_length=255, verbose_name='Tipo de habitación ofrecida')),
                ('number_guest_room_type', models.CharField(choices=[('Para 1 huésped', 'Para 1 huésped'), ('Para 2 huéspedes', 'Para 2 huéspedes'), ('Para 3 huéspede', 'Para 3 huéspedes'), ('Para 4 huéspedes', 'Para 4 huéspedes'), ('Para 5 huéspedes', 'Para 5 huéspedes'), ('Para 6 huéspedes', 'Para 6 huéspedes'), ('Para 7 huéspedes', 'Para 7 huéspedes'), ('Para 8 huéspedes', 'Para 8 huéspedes'), ('Para 9 huéspedes', 'Para 9 huéspedes'), ('Para 10 huéspedes', 'Para 10 huéspedes')], max_length=255, verbose_name='Número de huéspedes en habitación')),
                ('bed_type', models.CharField(choices=[('Cama individual', 'Cama individual'), ('Cama doble', 'Cama doble')], max_length=20, verbose_name='Tipo de cama')),
                ('bathroom', models.CharField(choices=[('Baño privado', 'Baño privado'), ('Baño compartido', 'Baño compartido')], max_length=20, verbose_name='Baño')),
                ('image', models.ImageField(help_text='Esta imagen acompañará tu oferta en los resultados de búsquedas', upload_to=hosts.models.get_lodging_image_search_path, verbose_name='Fotografía')),
                ('room_value', models.CharField(help_text='Precio en pesos colombianos', max_length=128, verbose_name='Precio')),
                ('additional_description', models.TextField(blank=True, null=True, verbose_name='Descripción adicional')),
                ('pub_date', models.DateTimeField(auto_now_add=True)),
                ('is_taked', models.BooleanField(default=False, help_text='Indica si esta oferta ya fue tomada por un usuario.  <br /> Este campo es solo para uso de actualización de una oferta cuando ya ha habido un acuerdo por ella. Si se selecciona, no aparecerá en los resultados de búsquedas. <br /> Des-seleccionéla en lugar de eliminar la oferta', verbose_name='Oferta tomada')),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('featured_amenities', models.ManyToManyField(help_text='Mantenga presionado "Control" (o "Command" en un Mac), y haga click en las opciones que desea selecionar.', to='host_information.FeaturesAmenities', verbose_name='Comodidades destacadas')),
                ('offered_services', models.ManyToManyField(help_text='Mantenga presionado "Control" (o "Command" en un Mac), y haga click en las opciones que desea selecionar.', related_name='lodgingoffers', to='host_information.OfferedServices', verbose_name='Servicios ofrecidos')),
                ('room_information', models.ManyToManyField(help_text='Mantenga presionado "Control" (o "Command" en un Mac), y haga click en las opciones que desea selecionar.', related_name='lodgingoffers', to='host_information.RoomInformation', verbose_name='Características de la habitación')),
            ],
        ),
        migrations.CreateModel(
            name='LodgingOfferImage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to=hosts.models.get_image_filename, verbose_name='Imagen')),
                ('lodging_offer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='lodgingofferimage', to='hosts.LodgingOffer')),
            ],
        ),
        migrations.CreateModel(
            name='StudiesOffert',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ad_title', models.CharField(max_length=255, verbose_name='Título de la oferta')),
                ('slug', models.SlugField(blank=True, max_length=100)),
                ('country', django_countries.fields.CountryField(max_length=2, verbose_name='País')),
                ('city', models.CharField(max_length=255, verbose_name='Ciudad')),
                ('address', models.CharField(max_length=255, verbose_name='Dirección')),
                ('latitude', models.CharField(blank=True, max_length=255, null=True, verbose_name='latitude')),
                ('longitude', models.CharField(blank=True, max_length=255, null=True, verbose_name='longitude')),
                ('maximum_quota', models.PositiveSmallIntegerField(verbose_name='Cupo máximo de estudiantes')),
                ('studies_type_offered', models.CharField(choices=[('Estudios de educación contínua', 'Estudios de educación contínua'), ('Técnica', 'Técnica'), ('Tecnología', 'Tecnología'), ('Pregrado', 'Pregrado'), ('Especialización', 'Especialización'), ('Maestría', 'Maestría'), ('Doctorado', 'Doctorado'), ('Movilidad académica', 'Movilidad académica')], max_length=255, verbose_name='Tipo de estudios ofertados')),
                ('academic_mobility_programs', models.CharField(choices=[('Semestre académico', 'Semestre académico'), ('Investigación', 'Investigación'), ('Rotaciones o prácticas', 'Rotaciones o prácticas'), ('Escuela de verano', 'Escuela de verano')], max_length=255, verbose_name='Programas de movilidad académica')),
                ('duration', models.CharField(max_length=255, verbose_name='Duración')),
                ('intensity', models.CharField(max_length=255, verbose_name='Intensidad')),
                ('modality', models.CharField(choices=[('Virtual', 'Virtual'), ('Presencial', 'Presencial')], max_length=20, verbose_name='Modalidad')),
                ('studies_value', models.CharField(help_text='Precio en pesos colombianos', max_length=128, verbose_name='Precio')),
                ('additional_description', models.TextField(blank=True, null=True, verbose_name='Descripción adicional')),
                ('photo', models.ImageField(help_text='Esta imagen acompañará tu oferta en los resultados de búsquedas', upload_to=hosts.models.get_image_search_path, verbose_name='Fotografía')),
                ('pub_date', models.DateTimeField(auto_now=True)),
                ('is_taked', models.BooleanField(default=False, help_text='Indica si esta oferta ya fue tomada por un usuario.  <br /> Este campo es solo para uso de actualización de una oferta cuando ya ha habido un acuerdo por ella. Si se selecciona, no aparecerá en los resultados de búsquedas. <br /> Des-seleccionéla en lugar de eliminar la oferta', verbose_name='Oferta tomada')),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('knowledge_topics', taggit.managers.TaggableManager(help_text='Una lista de temáticas separada por comas.', through='taggit.TaggedItem', to='taggit.Tag', verbose_name='Tópicos de conocimiento')),
            ],
        ),
        migrations.CreateModel(
            name='UploadStudyOffer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to=hosts.models.get_image_path, verbose_name='Seleccionar imagen')),
                ('order', models.IntegerField(default=0)),
                ('featured', models.BooleanField(default=False, help_text='Indica si la imagen aparecera en el carrusel', verbose_name='Destacada')),
                ('thumbnail', models.BooleanField(default=False)),
                ('active', models.BooleanField(default=True, help_text='Indica si una imagen de oferta esta habilitada o disponible', verbose_name='Activa')),
                ('updated', models.DateTimeField(auto_now=True)),
                ('start_date', models.DateTimeField(auto_now=True, null=True)),
                ('end_date', models.DateTimeField(auto_now=True, null=True)),
                ('study_offer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='uploadsstudyoffer', to='hosts.StudiesOffert')),
            ],
            options={
                'ordering': ['order', '-start_date', '-end_date'],
            },
        ),
    ]
