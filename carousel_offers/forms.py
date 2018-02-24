from django import forms
from bootstrap_datepicker.widgets import DatePicker

from .models import EducationalOfferCarousel, LodgingOfferCarousel, HomeCarousel


class DateInput(DatePicker):
    def __init__(self):
        DatePicker.__init__(self,format="%Y-%m-%d")
    def build_attrs(self, attrs, extra_attrs=None, **kwargs):
        attrs = dict(self.attrs, **kwargs)
        if extra_attrs:
            attrs.update(extra_attrs)
        return attrs


class HomeCarouselForm(forms.ModelForm):
    title = "Ingresar imágenes en el carrusel de la página de Inicio"

    class Meta:
        widgets = {
            'start_date': DateInput(),
            'end_date': forms.DateInput(
                            attrs={'id': 'end_date',
                                   'class': 'input-sm form-control',
                                   'type': 'text'
                         }),
        }
        model = HomeCarousel
        fields = ['title', 'image', 'order', 'url_link', 'header_text', 'text', 'active', 'featured',
                  'start_date', 'end_date', ]


class DateInput(DatePicker):
    def __init__(self):
        DatePicker.__init__(self,format="%Y-%m-%d")

    def build_attrs(self, attrs, extra_attrs=None, **kwargs):
        attrs = dict(self.attrs, **kwargs)
        if extra_attrs:
            attrs.update(extra_attrs)
        return attrs


class LodgingOfferCarouselForm(forms.ModelForm):
    title = "Ingresar imágenes en el carrusel de la página de Inicio"

    class Meta:
        widgets = {
            'start_date': DateInput(),
            'end_date': forms.DateInput(
                            attrs={'id': 'end_date',
                                   'class': 'input-sm form-control',
                                   'type': 'text'
                         }),
        }
        model = LodgingOfferCarousel
        fields = ['title','image', 'order', 'url_link', 'header_text', 'text', 'active', 'featured',
                  'start_date', 'end_date', ]


class EducationalOfferCarouselForm(forms.ModelForm):
    title = "Ingresar imágenes en el carrusel de la página de Inicio"

    class Meta:
        widgets = {
            'start_date': DateInput(),
            'end_date': forms.DateInput(
                            attrs={'id': 'end_date',
                                   'class': 'input-sm form-control',
                                   'type': 'text'
                         }),
        }
        model = EducationalOfferCarousel
        fields = ['title', 'image', 'order', 'url_link', 'header_text', 'text', 'active', 'featured',
                  'start_date', 'end_date', ]
