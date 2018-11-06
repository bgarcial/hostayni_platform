from django import forms
from .models import LodgingOffer, StudiesOffert, LodgingOfferImage, StudyOfferImage
from django_countries.widgets import CountrySelectWidget
from bootstrap_datepicker.widgets import DatePicker


class DateInput(DatePicker):
    def __init__(self):
        DatePicker.__init__(self,format="%Y-%m-%d")
    def build_attrs(self, attrs, extra_attrs=None, **kwargs):
        attrs = dict(self.attrs, **kwargs)
        if extra_attrs:
            attrs.update(extra_attrs)
        return attrs

class StudiesOffertForm(forms.ModelForm):
    #user = self.request.user
    ad = "Oferta de estudios"
    #scholarships = forms.ModelForm(queryset=Scholarship.objects.filter(created_by__username=user))
    offer_taked = ("\n"
                   " Indica si esta oferta ya fue finalizada por sus oferentes. Este campo es solo para uso de \n"
                   " actualización de una oferta cuando ésta ya ha caducado. "
                   " Si se selecciona, no aparecerá en los resultados de búsquedas. \n "
                   "Des-seleccionéla en lugar de eliminar la oferta ")

    class Meta:
        widgets = {
            'start_date': DateInput(),
            'finish_date': forms.DateInput(attrs={'id': 'datepicker2'}),
            'country': CountrySelectWidget(),
        }
        model = StudiesOffert
        fields = ('ad_title', 'country', 'city', 'formation_type_offered', 'modality',
                  'start_date', 'finish_date', 'place', 'duration', 'schedule', 'studies_value',
                  'discounts', 'status', 'organizers', 'sponsors', 'support', 'additional_description',
                  'photo', 'finished')
        # exclude = ('hosting_host_user',)
        # to put after: 'accreditations'


class StudyOfferImagesUploadForm(forms.ModelForm):
    class Meta:
        model = StudyOfferImage
        fields = ('image',)


class LodgingOfferForm(forms.ModelForm):
    title = "Crear oferta de alojamiento"
    offer_taked = ("\n"
     " Indica si esta oferta ya fue tomada por un usuario.Este campo es solo para uso de \n"
     " actualización de una oferta cuando ya ha habido un acuerdo por ella. "
     " Si se selecciona, no aparecerá en los resultados de búsquedas. \n "
     "Des-seleccionéla en lugar de eliminar la oferta ")

    class Meta:
        widgets = {
            'check_in': DateInput(),
            'check_out': forms.DateInput(attrs={'id': 'datepicker2'}),
            'country': CountrySelectWidget(),
        }
        model = LodgingOffer
        fields = ('ad_title', 'country', 'city', 'address', 'location_zone', 'check_in', 'check_out', 'offered_services',
                  'featured_amenities', 'room_type_offered', 'number_guest_room_type', 'photo',
                  'room_information', 'monthly_price', 'room_night_value', 'discounts',
                  'additional_description', 'is_taked')

    def __init__(self, *args, **kwargs):
        super(LodgingOfferForm, self).__init__(*args, **kwargs)


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
        attrs={'placeholder': 'Buscar por: Título, Ciudad, caracter de organización, '
                              'tipo de estudios, áreas de conocimiento, programa de movilidad académica,'
                              'duración, modalidad'}))
