from django.contrib import admin
from .models import Article, Category


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('id', 'author', 'title', 'updated', 'publish', 'draft', 'content' )
    list_display_links = ['updated']
    list_editable = ['title', 'draft',]
    list_filter = ['updated', 'timestamp']
    search_fields = ["title", 'content']


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['title', 'description']


