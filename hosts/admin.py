from django.contrib import admin

from django.contrib import admin
from .models import LodgingOffer, StudiesOffert, UploadStudyOffer
    #StudiesTypeOffered, StudiesOffertList, ,


@admin.register(UploadStudyOffer)
class UploadStudyOfferAdmin(admin.ModelAdmin):
    list_display = ['study_offer', 'image']

@admin.register(LodgingOffer)
class LodgingOfferAdmin(admin.ModelAdmin):
    list_display = ('id', 'ad_title', 'is_taked', 'room_type_offered',
        'number_guest_room_type', 'image', 'room_value',
        'additional_description', 'slug')

    list_editable = ('is_taked',)

@admin.register(StudiesOffert)
class StudiesOffertAdmin(admin.ModelAdmin):
    list_display = ('id', 'is_taked', 'ad_title', 'slug', 'tag_list',)
    list_editable = ('is_taked',)

    def get_queryset(self, request):
        return super(StudiesOffertAdmin, self).get_queryset(request).prefetch_related('knowledge_topics')

    def tag_list(self, obj):
        return u", ".join(o.name for o in obj.knowledge_topics.all())