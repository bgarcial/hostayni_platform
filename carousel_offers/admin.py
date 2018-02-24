from django.contrib import admin
from .models import LodgingOfferCarousel, EducationalOfferCarousel, HomeCarousel


# Register your models here.

@admin.register(HomeCarousel)
class SliderAdmin(admin.ModelAdmin):
    list_display = ["__str__", "order", "start_date", "end_date", "active", "featured"]
    list_editable = ['order', 'active', "start_date", "end_date",]
    class Meta:
        model = HomeCarousel


@admin.register(LodgingOfferCarousel)
class LodgingOfferSliderAdmin(admin.ModelAdmin):
    list_display = ["__str__", "order", "start_date", "end_date", "active", "featured"]
    list_editable = ['order', 'active', "start_date", "end_date",]

    class Meta:
        model = LodgingOfferCarousel


@admin.register(EducationalOfferCarousel)
class EducationalOfferSliderAdmin(admin.ModelAdmin):
    list_display = ["__str__", "order", "start_date", "end_date", "active", "featured"]
    list_editable = ['order', 'active', "start_date", "end_date",]

    class Meta:
        model = EducationalOfferCarousel