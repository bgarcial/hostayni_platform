from django.contrib.auth import get_user_model
from rest_framework import serializers
from django.urls import reverse_lazy

User = get_user_model()

class UserDisplaySerializer(serializers.ModelSerializer):
    # speak_languages = SpeakLanguagesDisplaySerializer()
    # Serializamos un metodo para que en el se vayan contando los seguidores de ese contacto
    # http://www.django-rest-framework.org/api-guide/fields/#serializermethodfield
    follower_count = serializers.SerializerMethodField()
    url = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = [
            'url',
            'full_name',
            'username',
            'email',
            'slug',
            'first_name',
            'last_name',
            'follower_count',
            'gender',
            # 'country_of_origin',
            'city_of_origin',
            # 'country_current_residence',
            'city_current_residence',
            'speak_languages',
            'phone_number',
            'address',
            'biography',
            'avatar',
            'date_of_birth',
            'user_type',
            'is_student',
            'is_professor',
            'is_executive',
            'is_study_host',
            'is_entrepreneurship_host',
            'is_hosting_host',
            'is_ayni_host',
            'is_daily_life_host',
            'entertainment_activities',
            'is_active',
        ]

    def get_follower_count(self, obj):
        # print(obj.email)
        return 0

    def get_url(self, obj):
        return reverse_lazy('accounts:detail', kwargs={"slug": obj.slug})
