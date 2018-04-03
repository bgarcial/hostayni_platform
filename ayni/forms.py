from django import forms
from .models import AyniOffer, AyniOfferImage
from django_countries.widgets import CountrySelectWidget

class AyniOfferForm(forms.ModelForm):

    title = "Crear oferta de ayni"
    offer_taked = ("\n" 
     " Indica si esta oferta ya fue tomada por un usuario.Este campo es solo para uso de \n"
     " actualización de una oferta cuando ya ha habido un acuerdo por ella. "
     " Si se selecciona, no aparecerá en los resultados de búsquedas. \n "
     "Des-seleccionéla en lugar de eliminar la oferta ")

    class Meta:
        widgets = {
            'country': CountrySelectWidget(),
        }
        model = AyniOffer
        fields = ('ad_title', 'country', 'city', 'offer_type', 'photo', 'address', 'maximum_quota', 'price', 'additional_description',
                  'is_taked',)


class AyniOfferImageForm(forms.ModelForm):

    image = forms.ImageField(label='Fotografía')

    class Meta:
        model = AyniOfferImage
        fields = ('image', )


class AyniOfferSearchForm(forms.Form):
    query = forms.CharField(label='', widget=forms.TextInput(
        attrs={'placeholder': 'Buscar por: '}))