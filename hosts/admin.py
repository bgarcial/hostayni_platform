from django.contrib import admin

from django.contrib import admin
from .models import LodgingOffer, StudiesOffert, StudyOfferImage, LodgingOfferImage
    #StudiesTypeOffered, StudiesOffertList, ,


@admin.register(LodgingOfferImage)
class StudyOfferImageAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'lodging_offer', 'image']
    list_editable = ('image',)

@admin.register(StudyOfferImage)
class StudyOfferImageAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'study_offer', 'image']
    # list_editable = ['order', 'active', 'featured']

    list_editable = ('image',)

@admin.register(LodgingOffer)
class LodgingOfferAdmin(admin.ModelAdmin):
    list_display = ('id', 'ad_title', 'is_taked', 'is_paid', 'room_type_offered', 'number_guest_room_type',
                     'monthly_price', 'room_night_value', 'additional_description', 'slug')

    list_editable = ('is_taked', 'is_paid')

@admin.register(StudiesOffert)
class StudiesOffertAdmin(admin.ModelAdmin):
    list_display = ('id', 'finished', 'is_paid', 'ad_title', 'slug',)
    list_editable = ('finished', 'is_paid')

    '''
    def get_queryset(self, request):
        return super(StudiesOffertAdmin, self).get_queryset(request).prefetch_related('knowledge_topics')

    def tag_list(self, obj):
        return u", ".join(o.name for o in obj.knowledge_topics.all())
    
    '''