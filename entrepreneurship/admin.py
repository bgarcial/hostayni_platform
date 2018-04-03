from django.contrib import admin
from .models import EntrepreneurshipOffer, EntrepreneurshipOfferImage

# Register your models here.

@admin.register(EntrepreneurshipOffer)
class EntrepreneurshipOfferAdmin(admin.ModelAdmin):
    list_display = ('id', 'ad_title', 'is_taked', 'is_paid', 'offer_type', 'price',
                     'country', 'city', 'date', 'url', 'contact_name')

    list_editable = ('is_taked', 'is_paid')


@admin.register(EntrepreneurshipOfferImage)
class EntrepreneurshipOfferImageAdmin(admin.ModelAdmin):
    list_display = ('id', 'entrepreneurship_offer', 'image',)

    list_editable = ('image',)