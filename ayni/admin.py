from django.contrib import admin
from .models import AyniOffer, AyniOfferImage

# Register your models here.

@admin.register(AyniOffer)
class AyniOfferAdmin(admin.ModelAdmin):
    list_display = ('id', 'ad_title', 'is_taked', 'is_paid', 'offer_type', 'price',
                     'country', 'city', 'address', 'maximum_quota',)

    list_editable = ('is_taked', 'is_paid')


@admin.register(AyniOfferImage)
class AyniOfferImageAdmin(admin.ModelAdmin):
    list_display = ('id', 'ayni_offer', 'image',)

    list_editable = ('image',)