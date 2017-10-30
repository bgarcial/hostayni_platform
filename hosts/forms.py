from django import forms
from .models import LodgingOffer, StudiesOffert, LodgingOfferImage, UploadStudyOffer
from django_countries.widgets import CountrySelectWidget
from django.forms import inlineformset_factory

class DateInput(forms.DateInput):
    input_type = 'date'

class StudiesOffertForm(forms.ModelForm):
    #user = self.request.user
    ad = "Oferta de estudios"
    #scholarships = forms.ModelForm(queryset=Scholarship.objects.filter(created_by__username=user))

    class Meta:
        model = StudiesOffert
        fields = ('ad_title', 'country', 'city', 'maximum_quota', 'knowledge_topics',
            'duration', 'intensity', 'studies_type_offered', 'academic_mobility_programs',
            'additional_description', 'photo', 'address', 'modality', 'studies_value', 'studies_value', 'is_taked')
        # exclude = ('hosting_host_user',)
        # to put after: 'accreditations'


class StudyOfferImagesUploadForm(forms.ModelForm):
    class Meta:
        model = UploadStudyOffer
        fields = ('image',)


class LodgingOfferForm(forms.ModelForm):
    title = "Crear oferta de alojamiento"
    # birth_year = forms.DateField(widget=forms.SelectDateWidget(years=LodgingOffer.BIRTH_YEAR_CHOICES))

    class Meta:
        widgets = {
            'check_in': DateInput(),
            'check_out': DateInput(),
            #'check_out': forms.DateInput(attrs={'class':'datepicker'}),
            'country': CountrySelectWidget(),
        }
        model = LodgingOffer
        fields = ('ad_title', 'country', 'city', 'address', 'lodging_offer_type', 'stars',
                  'check_in', 'check_out', 'offered_services', 'featured_amenities', 'room_type_offered',
                'number_guest_room_type', 'image', 'bed_type', 'bathroom', 'room_information', 'room_value',
                    'additional_description', 'is_taked')


class LodgingOfferImagesForm(forms.ModelForm):
    image = forms.ImageField(label='Fotografía')

    class Meta:
        model = LodgingOfferImage
        fields = ('image', )


class LodgingOfferSearchForm(forms.Form):
    query = forms.CharField(label='', widget=forms.TextInput(
        attrs={'placeholder': 'Buscar por: Ciudad, tipo de alojamiento, servicios ofrecidos, '
                              ' tipo de acomodación,'}))


class StudiesOffertSearchForm(forms.Form):
    query = forms.CharField(label='', widget=forms.TextInput(
        attrs={'placeholder': 'Buscar por: Título, Ciudad, caracter de organización,'
                              'tipo de estudios, áreas de conocimiento, programa de movilidad académica,'
                              'duración, modalidad, precio'}))