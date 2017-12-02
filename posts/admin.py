from django.contrib import admin
from .models import Post
from .forms import PostModelForm
# Register your models here.


@admin.register(Post)
class PostModelAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'content',)
    # form = PostModelForm

    class Meta:
        model = Post
