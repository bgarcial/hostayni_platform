from django.contrib import admin
from .models import Article, Comment, Category


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
     list_display = ('id', 'author', 'title', 'category', 'updated', 'publish', 'draft', 'content' )
     list_display_links = ['updated']
     list_editable = ['title', 'draft', 'category' ]
     list_filter =  ['updated', 'timestamp']
     search_fields = ["title", 'content']


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['title', 'description']

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('id' ,'name', 'email', 'article', 'created', 'active')
    list_filter = ('active', 'created', 'updated')
    search_fields = ('name', 'email', 'body')
