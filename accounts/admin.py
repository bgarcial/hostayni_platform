from __future__ import unicode_literals
from django.contrib import admin

from django.contrib.auth.admin import UserAdmin

from .models import (
    User, UserProfile, StudentProfile, ProfessorProfile, ExecutiveProfile,
    StudyHostProfile, InnovationHostProfile, EntertainmentHostProfile,
    OtherServicesHostProfile,
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
                    'gender',
                    'country_of_origin',
                    'city_of_origin',
                    'country_current_residence',
                    'city_current_residence',
                    'speak_languages',
                    #'email',
                    'phone_number',
                    'address',
                    'biography',
                    'avatar',
                    'date_of_birth',
                    'is_student',
                    'is_professor',
                    'is_executive',
                    'is_study_host',
                    'is_innovation_host',
                    'is_hosting_host',
                    'is_entertainment_host',
                    'is_other_services_host',
                ),
            }
        ),
    )
    # exclude = ('first_name', 'last_name')

# Change our UserAdmin class to inherit of our CustomUserAdmin created above (do not inherit of model.ModelAdmin)

@admin.register(User)
class UserAdmin(CustomUserAdmin):

    list_display = ('id',
                    'username',
                    'email',
                    'slug',
                    'user_type',
                    'first_name',
                    'last_name',
                    'gender',
                    'country_of_origin',
                    'phone_number',
                    'address',
                    'biography',
                    'date_of_birth',
                    'is_student',
                    'is_professor',
                    'is_executive',
                    'is_study_host',
                    "is_innovation_host",
                    "is_hosting_host",
                    "is_entertainment_host",
                    "is_other_services_host",
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


@admin.register(InnovationHostProfile)
class InnovationHostProfileAdmin(admin.ModelAdmin):
    list_display = ('id', 'user_id', 'slug', )


@admin.register(EntertainmentHostProfile)
class EntertainmentHostProfileAdmin(admin.ModelAdmin):
    list_display = ('id', 'user_id', 'slug', )


@admin.register(OtherServicesHostProfile)
class OtherServicesHostProfileAdmin(admin.ModelAdmin):
    list_display = ('id', 'user_id', 'slug', )


