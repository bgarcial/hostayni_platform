from django.contrib import admin
from .models import Article, Comment


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
     list_display = ('id', 'author', 'title', 'updated', 'timestamp', 'created_date',
        'published_date')
     list_display_links = ['updated']
     list_editable = ['title']
     list_filter =  ['updated', 'timestamp']
     search_fields = ["title", 'content']




@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('id' ,'name', 'email', 'article', 'created', 'active')
    list_filter = ('active', 'created', 'updated')
    search_fields = ('name', 'email', 'body')
