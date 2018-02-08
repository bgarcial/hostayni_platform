from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from django.forms.widgets import CheckboxSelectMultiple
from django import forms
from .models import (StudentProfile, ProfessorProfile, ExecutiveProfile,
                    StudyHostProfile,)

from django_countries.widgets import CountrySelectWidget

User = get_user_model()

class CustomUserChangeForm(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        model = get_user_model()


class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = get_user_model()
        fields = ('email',)


class UserCreateForm(UserCreationForm):

    class Meta:
        widgets = {
            'user_type':forms.RadioSelect(),
        }

        fields = ("email", "password1", "password2", "user_type",)
        model = get_user_model()


    def __init__(self, *args, **kwargs):
        super(UserCreateForm, self).__init__(*args, **kwargs)
        self.fields["email"].label = ""
        self.fields["password1"].label = ""
        self.fields["password2"].label = ""
        self.fields["user_type"].label = ""
        # self.fields["terms_and_conditions"].label = ""
        #email = forms.CharField(widget=forms.Textarea, label='')

    '''
    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 != password2:
            raise forms.ValidationError("Las contraseñas deben coincidir")
        return password2

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email__icontains=email).exists():
            raise forms.ValidationError("Este correo ya esta registrado")
        return email

    '''



class DateInput(forms.DateInput):
    input_type = 'date'


class UserUpdateForm(forms.ModelForm):
    # biography = forms.CharField(widget=forms.Textarea)

    class Meta:
        widgets = {
            # 'gender':forms.RadioSelect,
            'country_of_origin': CountrySelectWidget(),
            'country_current_residence': CountrySelectWidget(),
            # I can customize these https://github.com/SmileyChris/
            # django-countries#countryselectwidget
             'date_of_birth': DateInput(), #datepicker
             'creation_date': DateInput(), #datepicker
            #'date_of_birth': forms.DateInput(attrs={'class':'datepicker'})
        }

        fields = ("first_name", "last_name", "gender", "enterprise_name",
        "country_of_origin", "city_of_origin", "country_current_residence",
        "city_current_residence", 'speak_languages', "phone_number",
        "address", "biography", 'description', "avatar", "date_of_birth", "creation_date",
        'entertainment_activities', "is_student", "is_professor",
        "is_executive", "is_study_host", "is_hosting_host",)

        model = get_user_model()


class StudentProfileForm(forms.ModelForm):
    title = "Detalles del estudiante"

    class Meta:
        model = StudentProfile
        fields = ('origin_education_school', 'current_education_school',
                  'extra_occupation', 'educational_titles',
                  'complete_studies_school', 'knowledge_topics_choice',)


class ProfessorProfileForm(forms.ModelForm):
    title = "Detalles del Profesor"

    """
    occupation = forms.MultipleChoiceField(
        required=False,
        label='Ocupación',
        widget=CheckboxSelectMultiple(),
        choices=ProfessorProfile.OCCUPATION_CHOICES
    )
    """

    occupation = forms.ChoiceField(choices=[(x, x) for x in ['Catedrático', 'Investigador', 'Directivo Institucional',]])

    research_groups = forms.CharField(required=False,
                                      label='Grupos de Investigación',
                                      widget=forms.Textarea)
    autorship_publications = forms.CharField(required=False,
                                             label='Publicaciones',
                                             widget=forms.Textarea)

    class Meta:
        model = ProfessorProfile
        fields = ('occupation', 'origin_education_school',
            'current_education_school', 'educational_titles',
            'complete_studies_school', 'knowledge_topics_choice',
            'research_groups', 'autorship_publications',)


class ExecutiveProfileForm(forms.ModelForm):
    title = "Detalles del ejecutivo o emprendedor"
    # companies_to_visit = forms.CharField(widget=forms.Textarea)

    class Meta:
        model = ExecutiveProfile
        fields = ('enterprise_name',
        'educational_titles', 'complete_studies_school',
        'innovation_topics_choice', )


class StudyHostProfileForm(forms.ModelForm):
    title = "Detalles del anfitrión de estudios"
    widgets = {
            'institute_character':forms.RadioSelect,
    }

    high_quality_accreditations = forms.MultipleChoiceField(
        required=False,
        label='Acreditaciones de alta calidad',
        widget=CheckboxSelectMultiple(),
        choices=StudyHostProfile.ACCREDITATIONS_CHOICES,
    )

    knowledge_topics = forms.CharField(label='Áreas de conocimiento',
                                widget=forms.TextInput(attrs={
                                    'placeholder': 'Una lista de temas separada por comas'}))




    class Meta:
        model = StudyHostProfile
        fields = ('institution_type', 'institute_character',
            'high_quality_accreditations', 'students_number',
            'rankings_classification', 'knowledge_topics', )
        #exclude = ('studies_offert_list', )




'''

class HostingHostProfileForm(forms.ModelForm):
    title = "También eres anfitrión de alojamiento"

    class Meta:
        model = HostingHostProfile

        fields = ( )

        fields = ('additional_description', )
'''

