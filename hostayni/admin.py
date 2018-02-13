from django.contrib import admin
from .models import Slider


@admin.register(Slider)
class SliderAdmin(admin.ModelAdmin):
    list_display = ["__str__", "order", "start_date", "end_date", "active", "featured"]
    list_editable = ['order', 'active', "start_date", "end_date",]
    class Meta:
        model = Slider
