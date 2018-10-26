from __future__ import unicode_literals
from django.contrib import admin

from django.contrib.auth.admin import UserAdmin

from .models import (
    User, UserProfile, StudentProfile, ProfessorProfile, ExecutiveProfile,
    StudyHostProfile, EntrepreneurshipHostProfile, AyniHostProfile,
    DailyLifeHostProfile,
)

from .forms import CustomUserChangeForm, CustomUserCreationForm

# Inherit of the original UserAdmin for use the customized forms
class CustomUserAdmin(UserAdmin):
    form = CustomUserChangeForm
    add_form = CustomUserCreationForm

    fieldsets = UserAdmin.fieldsets + (
        (
            None, {
                'classes':('wide',),
                'fields':(
                    'slug',
                    #'first_name',
                    #'last_name',
                    # 'display_name',
                    "full_name",
                    'gender',
                    'country_of_origin',
                    'city_of_origin',
                    'country_current_residence',
                    'city_current_residence',
                    'speak_languages',
                    'entrepreneurship_areas',
                    #'email',
                    'phone_number',
                    'address',
                    'biography',
                    'avatar',
                    'date_of_birth',
                    # 'user_type',
                    'is_student',
                    'is_employed',
                    'is_independent',
                    'educational_titles',
                    'complete_studies_school',
                ),
            }
        ),
    )
    # exclude = ('first_name', 'last_name')

# Change our UserAdmin class to inherit of our CustomUserAdmin created above (do not inherit of model.ModelAdmin)

@admin.register(User)
class UserAdmin(CustomUserAdmin):

    list_display = (
                    'full_name',
                    'username',
                    'email',
                    'slug',
                    # 'user_type',
                    # 'first_name',
                    # 'last_name',
                    'gender',
                    'country_of_origin',
                    'phone_number',
                    'address',
                    'biography',
                    'date_of_birth',
                    'is_student',
                    'is_employed',
                    'is_independent',
    )


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('id', 'user_id', )


@admin.register(StudentProfile)
class StudentProfileAdmin(admin.ModelAdmin):
    list_display = ('id', 'user_id', 'slug', )


@admin.register(ProfessorProfile)
class ProfessorProfileAdmin(admin.ModelAdmin):
    list_display = ('id', 'user_id', 'slug', )

@admin.register(ExecutiveProfile)
class ExecutiveProfileAdmin(admin.ModelAdmin):
    list_display = ('id', 'user_id', 'slug', )


@admin.register(StudyHostProfile)
class StudyHostProfileAdmin(admin.ModelAdmin):
    list_display = ('id', 'user_id', 'slug', )


@admin.register(EntrepreneurshipHostProfile)
class InnovationHostProfileAdmin(admin.ModelAdmin):
    list_display = ('id', 'user_id', 'slug', )


@admin.register(AyniHostProfile)
class EntertainmentHostProfileAdmin(admin.ModelAdmin):
    list_display = ('id', 'user_id', 'slug', )


@admin.register(DailyLifeHostProfile)
class OtherServicesHostProfileAdmin(admin.ModelAdmin):
    list_display = ('id', 'user_id', 'slug', )


