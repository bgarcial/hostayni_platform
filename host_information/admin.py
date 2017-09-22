from __future__ import unicode_literals
from django.contrib import admin
from .models import (
    SpeakLanguages, OfferedServices,
    EntertainmentActivities, LodgingOfferType,
    RoomInformation, FeaturesAmenities
)

@admin.register(SpeakLanguages)
class SpeakLanguagesAdmin(admin.ModelAdmin):

    list_display = ('id', 'name',)

@admin.register(EntertainmentActivities)
class EntertainmentActivitiesAdmin(admin.ModelAdmin):

    list_display = ('id', 'name', 'description')


@admin.register(FeaturesAmenities)
class FeaturesAmenitiesAdmin(admin.ModelAdmin):

    list_display = ('id', 'name', 'description')


@admin.register(OfferedServices)
class OfferedServicesAdmin(admin.ModelAdmin):

    list_display = ('id', 'name', 'description')


@admin.register(RoomInformation)
class RoomInformationAdmin(admin.ModelAdmin):

    list_display = ('id', 'name', 'description')


@admin.register(LodgingOfferType)
class LodgingOfferTypeAdmin(admin.ModelAdmin):

    list_display = ('id', 'name',)
