from django.contrib import admin
from .models import LodgingOfferCarousel, EducationalOfferSlider


# Register your models here.
@admin.register(LodgingOfferCarousel)
class LodgingOfferSliderAdmin(admin.ModelAdmin):
    list_display = ["__str__", "order", "start_date", "end_date", "active", "featured"]
    list_editable = ['order', 'active', "start_date", "end_date",]

    class Meta:
        model = LodgingOfferCarousel


@admin.register(EducationalOfferSlider)
class EducationalOfferSliderAdmin(admin.ModelAdmin):
    list_display = ["__str__", "order", "start_date", "end_date", "active", "featured"]
    list_editable = ['order', 'active', "start_date", "end_date",]

    class Meta:
        model = EducationalOfferSlider