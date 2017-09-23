from django.conf.urls import url
from . import views

urlpatterns = [

    url(r'^$', views.ArticleListView.as_view(),name='article_list'),

    url(r'^article/new/$', views.CreateArticleView.as_view(),
        name='article_new'),

    url(r'^article/(?P<slug>[\w.\-]+)/$', views.article_detail,
        name='article_detail'),

    url(r'^article/(?P<slug>[\w.\-]+)/share/$', views.article_share,
        name='article_share'),

    url(r'^articles/by/u/@(?P<email>[-\w]+)/$',
        views.articles_by_user, name='list'
    ),

    # url(r'^article/(?P<pk>\d+)/$', views.ArticleDetailView.as_view(),
    #    name='article_detail'),



    url(r'^article/(?P<slug>[\w.\-]+)/edit/$',
        views.ArticleUpdateView.as_view(), name='article_edit'),

    url(r'^article/(?P<slug>[\w.\-]+)/remove/$', views.ArticleDeleteView.as_view(), name='article_remove'),


    #url(r'^drafts/$', views.ArticleDraftListView.as_view(),
    #    name='article_draft_list'),

    #url(r'^article/(?P<pk>\d+)/comment/$', views.add_comment_to_article,
    #    name='add_comment_to_article'),

    #url(r'^comment/(?P<pk>\d+)/approve/$', views.comment_approve,
    #    name='comment_approve'),

    #url(r'^comment/(?P<pk>\d+)/remove/$', views.comment_remove,
    #    name='comment_remove'),

    url(r'^article/(?P<slug>[\w.\-]+)/publish/$', views.article_publish,
        name='article_publish'),

]
