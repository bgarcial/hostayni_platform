from django import forms
from blog.models import Article, Comment
from django.utils.text import slugify



class EmailPostForm(forms.Form):
    name = forms.CharField(max_length=25)
    email = forms.EmailField()
    to = forms.EmailField()
    comments = forms.CharField(required=False,
                               widget=forms.Textarea)


YEARS = [x for x in range(1980, 2050)]


class ArticleForm(forms.ModelForm):
    # title = forms.CharField(
    #        max_length=120,
    #        label='Titulo',
    #        help_text='some help text',
    #        error_messages={
    #            "required": "El campo título es requerido."
    #        }
    # )

    content = forms.CharField(widget=forms.Textarea)
    ad = "Nuevo artículo"
    # publish = forms.DateField(initial="2010-11-20", widget=forms.SelectDateWidget(years=YEARS))
    # publish = forms.DateField(widget=forms.DateInput(format='%d/%m/%Y'))
    # publish = forms.DateField(widget=forms.)
    class Meta:
        model = Article
        fields = [
            'title',
            'content',
            'image',
            'draft',
            # 'publish',
        ]
        labels = {
            "title": "Título",
            "content": "Este es el contenido",
        }
        help_texts = {
            "title": "Título",
            "content": "Este es el contenido",
        }
        error_messages = {
            #"title": {
            #    "max_lenght": "Este titulo es muy largo",
            #    "required": "El campo título es requerido.",
            #},
            "content": {
                "max_lenght": "Este contenido es muy largo",
                "required": "El campo content es requerido.",
                # "unique": "El campo content debe ser unico.",
            },
        }



        '''
        widgets = {
            #'publish': forms.DateInput(attrs={'class':'datepicker'})
            # 'title':forms.TextInput(attrs={'class':'textinputclass'}),
            # 'text': forms.Textarea(attrs={'class':'editable medium-editor-textarea postcontent'})
        }
        '''

    def __init__(self, *args, **kwargs):
        super(ArticleForm, self).__init__(*args, **kwargs)
        self.fields['title'].widget = forms.Textarea()
        # self.fields['publish'].widget = forms.DateField()
        self.fields['title'].error_messages = {
            "max_lenght": "Este titulo es muy largo",
            "required": "El campo título es requerido.",
        }
        self.fields['content'].error_messages = {
            "max_lenght": "Este contenido es muy largo",
            "required": "El campo content es requerido.",
        }

        for field in self.fields.values():
            field.error_messages = {
                'required': "Tu sabes que {fieldname} is required".format(fieldname=field.label),
            }



    '''
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






class ReviewForm(forms.Form):
    pass

class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ('name', 'email', 'body')

        widgets = {
            'name':forms.TextInput(attrs={'class':'textinputclass'}),
            'body': forms.Textarea(attrs={'class':'editable medium-editor-textarea '})

        }
