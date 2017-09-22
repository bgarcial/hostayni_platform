from __future__ import unicode_literals
from django.db import models


# Research Groups
# Accreditations
# Scholarships
# Publications

class SpeakLanguages(models.Model):

    name = models.CharField(max_length=255, null=False, blank=False)

    class Meta:
        verbose_name = "Idiomas"
        verbose_name_plural = "Idiomas"

    def __str__(self):
        return self.name


class EntertainmentActivities(models.Model):

    name = models.CharField(max_length=255, null=False, blank=False)
    description = models.CharField(max_length=255, null=True, blank=True)

    class Meta:
        verbose_name = "Actividades de Entretenimiento"
        verbose_name_plural = "Actividades de Entretenimiento"

    def __str__(self):
        return self.name


class LodgingOfferType(models.Model):

    name = models.CharField(max_length=100, null=False, blank=False)

    class Meta:
        verbose_name = "Tipo de Oferta de Alojamiento"
        verbose_name_plural = "Tipo de Ofertas de Alojamiento"

    def __str__(self):
        return self.name


class OfferedServices(models.Model):

    name = models.CharField(max_length=100, null=False, blank=False)
    description = models.CharField(max_length=255, null=True, blank=True)

    class Meta:
        verbose_name = "Servicios ofrecidos"
        verbose_name_plural = "Servicios ofrecidos"

    def __str__(self):
        return self.name


class FeaturesAmenities(models.Model):

    name = models.CharField(max_length=100, null=False, blank=False)

    description = models.CharField(max_length=255, null=True, blank=True)

    class Meta:
        verbose_name = "Comodidades destacadas"
        verbose_name_plural = "Comodidades destacadas"

    def __str__(self):
        return self.name


class RoomInformation(models.Model):

    name = models.CharField(
        max_length=100,
        null=False,
        blank=False
    )

    description = models.CharField(
        max_length=255,
        null=True,
        blank=True
    )

    class Meta:
        verbose_name = "Características del cuarto"
        verbose_name_plural = "Características del cuarto"

    def __str__(self):
        return self.name
