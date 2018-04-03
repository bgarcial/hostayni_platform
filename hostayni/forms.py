from django import forms
from bootstrap_datepicker.widgets import DatePicker

from hostayni.models import Slider


class ContactForm(forms.Form):
    contact_name = forms.CharField(required=True)
    contact_email = forms.EmailField(required=True)
    form_content = forms.CharField(required=True, widget=forms.Textarea(attrs={'placeholder':'Nos encantará leerte'}))

    def __init__(self, *args, **kwargs):
        super(ContactForm, self).__init__(*args, **kwargs)
        self.fields['contact_name'].label = "Tu nombre:"
        self.fields['contact_email'].label = "Tu correo electrónico:"
        self.fields['form_content'].label = "¿Qué nos quieres decir?"



class DateInput(DatePicker):
    def __init__(self):
        DatePicker.__init__(self,format="%Y-%m-%d")
    def build_attrs(self, attrs, extra_attrs=None, **kwargs):
        attrs = dict(self.attrs, **kwargs)
        if extra_attrs:
            attrs.update(extra_attrs)
        return attrs


class HomeSliderForm(forms.ModelForm):
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
        model = Slider
        fields = ['title', 'image', 'order', 'url_link', 'header_text', 'text', 'active', 'featured',
                  'start_date', 'end_date', ]

