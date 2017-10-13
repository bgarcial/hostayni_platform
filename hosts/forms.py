from django import forms
from .models import LodgingOffer, StudiesOffert
from django_countries.widgets import CountrySelectWidget

class DateInput(forms.DateInput):
    input_type = 'date'

class StudiesOffertForm(forms.ModelForm):
    #user = self.request.user
    ad = "Oferta de estudios"
    #scholarships = forms.ModelForm(queryset=Scholarship.objects.filter(created_by__username=user))

    class Meta:
        model = StudiesOffert
        fields = ('ad_title', 'country', 'city',
            'institute_character', 'maximum_quota', 'knowledge_topics',
            'duration', 'studies_type_offered', 'academic_mobility_programs',
            'additional_description', 'photo', 'address', 'modality', 'studies_value',
                  'studies_value')
        # exclude = ('hosting_host_user',)
        # to put after: 'accreditations'



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
                  'check_in', 'check_out', 'offered_services',
            'featured_amenities', 'room_type_offered',
            'number_guest_room_type', 'bed_type', 'bathroom',
            'room_information', 'image', 'room_value',
            'additional_description',)

        # exclude = ('hosting_host_user',)


class LodgingOfferSearchForm(forms.Form):
    query = forms.CharField(label='', widget=forms.TextInput(
        attrs={'placeholder': 'Buscar por: Título, Ciudad, tipo de alojamiento, # de estrellas, servicios ofrecidos, '
                              'comodidades destacadas, tipo de acomodación, tipo de cama, características de la habitación,'
                              'baño, precio ($COP)'}))


class StudiesOffertSearchForm(forms.Form):
    query = forms.CharField(label='')