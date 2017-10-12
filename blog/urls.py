from django.conf.urls import url
from . import views

from .views import (
    article_create,
    article_list,
    article_delete,
    artic_detail,
    article_update,
    article_detail,
    article_share,
    article_publish,
    categories,
)

urlpatterns = [


    # ---*** URLs with fbv ***---
    url(r'^article/create/$', article_create, name='create'),
    # url(r'^article/new/$', views.CreateArticleView.as_view(), name='article_new'),
    # MOre below

    url(r'^articles/categoria/(\d+)$', categories, name='categories'),

    url(r'^article/(?P<slug>[\w.\-]+)/edit/$', article_update, name='update'),
    url(r'^article/(?P<slug>[\w.\-]+)/delete/$', article_delete, name='delete'),
    url(r'^article/(?P<slug>[\w.\-]+)/$', artic_detail, name='detail'),





    # ---*** URLs with fbv ***---

    url(r'^$', views.ArticleListView.as_view(),name='article_list'),
    # url(r'^$', article_list, name='article_list'),



    # url(r'^article/(?P<slug>[\w.\-]+)/$', article_detail, name='detail'),

    url(r'^article/(?P<slug>[\w.\-]+)/share/$', article_share,
        name='article_share'),

    url(r'^articles/by/u/@(?P<email>[-\w]+)/$',
        views.articles_by_user, name='list'
    ),

    # url(r'^article/(?P<pk>\d+)/$', views.ArticleDetailView.as_view(),
    #    name='article_detail'),



    # url(r'^article/(?P<slug>[\w.\-]+)/edit/$', views.ArticleUpdateView.as_view(), name='article_edit'),

    url(r'^article/(?P<slug>[\w.\-]+)/remove/$', views.ArticleDeleteView.as_view(), name='article_remove'),


    #url(r'^drafts/$', views.ArticleDraftListView.as_view(),
    #    name='article_draft_list'),

    #url(r'^article/(?P<pk>\d+)/comment/$', views.add_comment_to_article,
    #    name='add_comment_to_article'),

    #url(r'^comment/(?P<pk>\d+)/approve/$', views.comment_approve,
    #    name='comment_approve'),

    #url(r'^comment/(?P<pk>\d+)/remove/$', views.comment_remove,
    #    name='comment_remove'),

    url(r'^article/(?P<slug>[\w.\-]+)/publish/$', article_publish,
        name='article_publish'),

]
