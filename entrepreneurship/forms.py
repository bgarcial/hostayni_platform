from django import forms
from .models import EntrepreneurshipOffer, EntrepreneurshipOfferImage
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


class EntrepreneurshipOfferForm(forms.ModelForm):
    title = "Crear evento"
    offer_taked = ("\n" 
     " Indica si esta oferta ya fue tomada por un usuario.Este campo es solo para uso de \n"
     " actualización de una oferta cuando ya ha habido un acuerdo por ella. "
     " Si se selecciona, no aparecerá en los resultados de búsquedas. \n "
     "Des-seleccionéla en lugar de eliminar la oferta ")

    class Meta:
        widgets = {
            'date': DateInput(),
            'country': CountrySelectWidget(),
        }
        model = EntrepreneurshipOffer
        fields = ('ad_title', 'price', 'country', 'city', 'date',
                  'photo', 'discounts', 'status', 'additional_description', 'is_taked',)


class EntrepreneurshipOfferImagesForm(forms.ModelForm):
    image = forms.ImageField(label='Fotografía')

    class Meta:
        model = EntrepreneurshipOfferImage
        fields = ('image', )


class EntrepreneurshipOfferSearchForm(forms.Form):
    query = forms.CharField(label='', widget=forms.TextInput(
        attrs={'placeholder': 'Buscar por: Ciudad, Tipo de oferta, país, título '}))