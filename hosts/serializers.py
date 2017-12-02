from rest_framework import serializers
from .models import LodgingOffer, StudiesOffert


class LodgingOfferSerializer(serializers.ModelSerializer):
    class Meta:
        model = LodgingOffer
        fields = ('url', 'created_by', 'ad_title', 'country', 'city',
            'address', 'latitude', 'longitude', 'lodging_offer_type', 'stars', 'check_in',
                  'check_out',
            'offered_services', 'featured_amenities', 'room_type_offered',
             'number_guest_room_type', 'bed_type', 'bathroom',
             'room_information', 'image', 'room_value',
             'additional_description' )


class StudiesOffertSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudiesOffert
        fields = ('url', 'created_by', 'ad_title', 'country', 'city',
            'address', 'latitude', 'longitude',
            'maximum_quota', 'studies_type_offered',
            'academic_mobility_programs', 'photo', 'duration', 'studies_value',
            'additional_description' )