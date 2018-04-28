from django import forms
from blog.models import Article
from django.utils.text import slugify
from pagedown.widgets import PagedownWidget


class ArticleForm(forms.ModelForm):

    content = forms.CharField(label='Contenido', widget=forms.Textarea(attrs={'placeholder': 'Contenido'}))
    # content = forms.CharField(label='Contenido', widget=PagedownWidget())
    ad = "Nuevo artículo"

    class Meta:
        model = Article
        fields = [
            'title',
            'content',
            'category',
            'image',
            'draft',
            # 'publish',
        ]
        labels = {
            "title": "Título",
            "content": "Contenido",
        }
        help_texts = {
            "content": "Título",
            "content": "Este es el contenido",
        }
        error_messages = {
            #"title": {
            #    "max_lenght": "Este titulo es muy largo",
            #    "required": "El campo título es requerido.",
            #},
            "content": {
                "max_lenght": "Este contenido es muy largo",
                "required": "El campo contenido es requerido.",
                # "unique": "El campo content debe ser unico.",
            },
        }



    def __init__(self, *args, **kwargs):
        super(ArticleForm, self).__init__(*args, **kwargs)
        # self.fields['title'].widget = forms.Textarea()
        # self.fields['publish'].widget = forms.DateField()
        self.fields['title'].error_messages = {
            "max_lenght": "Este titulo es muy largo",
            "required": "El campo título es requerido.",
        }
        self.fields['content'].error_messages = {
            "max_lenght": "Este contenido es muy largo",
            "required": "El campo contenido es requerido.",
        }

        for field in self.fields.values():
            field.error_messages = {
                'required': "Tu sabes que {fieldname} is required".format(fieldname=field.label),
            }

    '''
    def clean(self):
        cleaned_data = super(ArticleForm, self).clean()
        title = cleaned_data.get('title')
        content = cleaned_data.get('content')
        image = cleaned_data.get('image')
        draft = cleaned_data.get('draft')
        if not title and not content and not image and not draft:
            raise forms.ValidationError('You have to write something!')

    
    def clean_title(self, *args, **kwargs):
        title = self.cleaned_data.get('title')
        print(title)
        #raise forms.ValidationError("Nope")
        return title
    
    def save(self, commit=True, *args, **kwargs):
        obj = super(ArticleForm, self).save(commit=False, *args, **kwargs)
        #
        # obj.publish = "2016-10-01"
        # obj.title = 'New title'
        #obj.title = slugify(obj.title)
        if commit:
            obj.save()
        return obj
    '''




