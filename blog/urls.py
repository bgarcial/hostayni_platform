from django.conf.urls import url
from . import views

from .views import (
    article_create,
    article_delete,
    artic_detail,
    article_update,
    # article_detail,
    categories,
)

urlpatterns = [


    # ---*** URLs with fbv ***---
    # url(r'^article/create/$', article_create, name='create'),
    url(r'^article/new/$', views.CreateArticleView.as_view(), name='new'),
    # MOre below

    url(r'^articles/categoria/(\d+)$', categories, name='categories'),

    url(r'^article/(?P<slug>[\w.\-]+)/edit/$', article_update, name='update'),
    # url(r'^article/(?P<slug>[\w.\-]+)/delete/$', article_delete, name='delete'),
    url(r'^article/(?P<slug>[\w.\-]+)/$', artic_detail, name='detail'),





    # ---*** URLs with fbv ***---

    # url(r'^$', views.ArticleListView.as_view(), name='article_list'),
    url(r'^$', views.article_list, name='article_list'),
    url(r'^tag/(?P<tag_slug>[-\w]+)/$', views.article_list,
                name='post_list_by_tag'),
    # both patterns point to the same view, but we are
    # naming them differently. The first pattern will call
    # the article_list view without any optional parameters,
    # while the second pattern will call the view with the
    # tag_slug parameter.


    url(r'^category/(\d+)$', views.categories, name='category'),


    # url(r'^article/(?P<slug>[\w.\-]+)/$', article_detail, name='detail'),

    url(r'^articles/by/u/@(?P<username>[-\w]+)/$',views.articles_by_user, name='list'),

    # url(r'^article/(?P<pk>\d+)/$', views.ArticleDetailView.as_view(),
    #    name='article_detail'),



    # url(r'^article/(?P<slug>[\w.\-]+)/edit/$', views.ArticleUpdateView.as_view(), name='article_edit'),

    url(r'^article/(?P<slug>[\w.\-]+)/remove/$', views.ArticleDeleteView.as_view(), name='article_remove'),



]
