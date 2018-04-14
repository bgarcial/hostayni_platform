from django import forms
from .models import Post


class PostModelForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = [
            # "user",
            "content"
        ]
        # exclude = ["user"]

    def __init__(self, *args, **kwargs):
        super(PostModelForm, self).__init__(*args, **kwargs)
        self.fields["content"].label = ""

    '''
    def clean_content(self, *args, **kwargs):
        # Basic validation
        # https://docs.djangoproject.com/en/1.11/ref/forms/validation/#cleaning-a-specific-field-attribute
        content = self.cleaned_data.get("content")
        if content == "abc":
            raise forms.ValidationError("Cannot be ABC")
        return content
    '''