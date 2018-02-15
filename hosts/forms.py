from django import forms
from .models import LodgingOffer, StudiesOffert, LodgingOfferImage, StudyOfferImage
from django_countries.widgets import CountrySelectWidget
from bootstrap_datepicker.widgets import DatePicker



class StudiesOffertForm(forms.ModelForm):
    #user = self.request.user
    ad = "Oferta de estudios"
    #scholarships = forms.ModelForm(queryset=Scholarship.objects.filter(created_by__username=user))
    offer_taked = ("\n"
                   " Indica si esta oferta ya fue tomada por un usuario.Este campo es solo para uso de \n"
                   " actualización de una oferta cuando ya ha habido un acuerdo por ella. "
                   " Si se selecciona, no aparecerá en los resultados de búsquedas. \n "
                   "Des-seleccionéla en lugar de eliminar la oferta ")

    class Meta:
        model = StudiesOffert
        fields = ('ad_title', 'country', 'city', 'maximum_quota', 'knowledge_topics',
            'duration', 'intensity', 'studies_type_offered', 'academic_mobility_programs',
            'additional_description', 'photo', 'address', 'modality', 'studies_value', 'studies_value', 'is_taked')
        # exclude = ('hosting_host_user',)
        # to put after: 'accreditations'


class StudyOfferImagesUploadForm(forms.ModelForm):
    class Meta:
        model = StudyOfferImage
        fields = ('image',)


class DateInput(DatePicker):
    def __init__(self):
        DatePicker.__init__(self,format="%Y-%m-%d")
    def build_attrs(self, attrs, extra_attrs=None, **kwargs):
        attrs = dict(self.attrs, **kwargs)
        if extra_attrs:
            attrs.update(extra_attrs)
        return attrs

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
            'check_out': DateInput(),
            'country': CountrySelectWidget(),
        }
        model = LodgingOffer
        fields = ('ad_title', 'country', 'city', 'address', 'lodging_offer_type' , 'lodging_offer_type_org', 'stars',
                  'check_in', 'check_out', 'offered_services', 'featured_amenities', 'room_type_offered',
                'number_guest_room_type', 'photo', 'bed_type', 'bathroom', 'room_information', 'room_value',
                    'additional_description', 'is_taked')

    def __init__(self, *args, **kwargs):
        super(LodgingOfferForm, self).__init__(*args, **kwargs)
        self.fields['check_in'].widget.attrs['class'] = 'input-group input-daterange'
        self.fields['check_out'].widget.attrs['class'] = 'input-group input-daterange'



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