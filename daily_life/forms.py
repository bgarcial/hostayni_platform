from django import forms
from .models import (DailyLifeOffer, DailyLifeOfferImage)
from django_countries.widgets import CountrySelectWidget


class DailyLifeOfferForm(forms.ModelForm):

    title = "Crear oferta de vida diaria"
    offer_taked = ("\n" 
     " Indica si esta oferta ya fue tomada por un usuario.Este campo es solo para uso de \n"
     " actualización de una oferta cuando ya ha habido un acuerdo por ella. "
     " Si se selecciona, no aparecerá en los resultados de búsquedas. \n "
     "Des-seleccionéla en lugar de eliminar la oferta ")

    class Meta:
        widgets = {
            'country': CountrySelectWidget(),
        }
        model = DailyLifeOffer
        fields = ('ad_title', 'country', 'city', 'offer_type', 'photo', 'address', 'price', 'additional_description',
                  'is_taked',)


class DailyLifeOfferImagesForm(forms.ModelForm):

    image = forms.ImageField(label='Fotografía')

    class Meta:
        model = DailyLifeOfferImage
        fields = ('image', )


class DailyLifeOfferSearchForm(forms.Form):
    query = forms.CharField(label='', widget=forms.TextInput(
        attrs={'placeholder': 'Buscar por: País, ciudad, Tipo de Oferta '}))