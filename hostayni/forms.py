from django import forms
from bootstrap_datepicker.widgets import DatePicker

from carousel_offers.models import HomeCarousel

class ContactForm(forms.Form):
    contact_name = forms.CharField(required=True)
    contact_email = forms.EmailField(required=True)
    form_content = forms.CharField(required=True, widget=forms.Textarea(attrs={'placeholder':'Nos encantará leerte'}))

    def __init__(self, *args, **kwargs):
        super(ContactForm, self).__init__(*args, **kwargs)
        self.fields['contact_name'].label = "Tu nombre:"
        self.fields['contact_email'].label = "Tu correo electrónico:"
        self.fields['form_content'].label = "¿Qué nos quieres decir?"






