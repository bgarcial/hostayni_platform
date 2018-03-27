from django.contrib import admin
from .models import DailyLifeOffer, DailyLifeOfferImage

# Register your models here.

@admin.register(DailyLifeOffer)
class DailyLifeOfferAdmin(admin.ModelAdmin):
    list_display = ('id', 'ad_title', 'is_taked', 'is_paid', 'offer_type', 'price',
                     'country', 'city', 'address', 'additional_description')

    list_editable = ('is_taked', 'is_paid')


@admin.register(DailyLifeOfferImage)
class DailyLifeOfferImageAdmin(admin.ModelAdmin):
    list_display = ('id', 'daily_life_offer', 'image',)

    list_editable = ('image',)