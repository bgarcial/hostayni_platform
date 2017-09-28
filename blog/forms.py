from django import forms
from blog.models import Article, Comment


class EmailPostForm(forms.Form):
    name = forms.CharField(max_length=25)
    email = forms.EmailField()
    to = forms.EmailField()
    comments = forms.CharField(required=False,
                               widget=forms.Textarea)


class ArticleForm(forms.ModelForm):
    content = forms.CharField(widget=forms.Textarea)
    ad = "Nuevo artículo"
    class Meta:
        model = Article
        fields = [
            'title',
            'content',
            'image',
            'draft',
            'publish',
        ]

        '''
        widgets = {
            'title':forms.TextInput(attrs={'class':'textinputclass'}),
            'text': forms.Textarea(attrs={'class':'editable medium-editor-textarea postcontent'})

        }
        '''


class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ('name', 'email', 'body')

        widgets = {
            'name':forms.TextInput(attrs={'class':'textinputclass'}),
            'body': forms.Textarea(attrs={'class':'editable medium-editor-textarea '})

        }
