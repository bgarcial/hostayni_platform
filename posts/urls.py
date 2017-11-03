from django.conf.urls import url
from django.views.generic.base import RedirectView

from .views import (
    PostCreateView,
    PostListView,
    PostDetailView,
    # PostUpdateView,
    # PostDeleteView,
    # RepostView,
    )

from hostayni.views import SearchView

# view this guide
# https://github.com/codingforentrepreneurs/Guides/blob/master/all/common_url_regex.md

urlpatterns = [
    # https://docs.djangoproject.com/en/1.11/ref/class-based-views/base/#redirectview
    #url(r'^$', RedirectView.as_view(url="/post/search/")),

    # url(r'^$', post_list_view, name='list'),
    # Listar los posts en el sistema (a quien sigo y los mios ya por JQuery y las APIViews)
    url(r'^$', PostListView.as_view(), name='list'), # /post/

    # Buscando en Hostayni social seria /post/search/
    url(r'^search/$', SearchView.as_view(), name='search'), #

    url(r'^create/$', PostCreateView.as_view(), name='create'), # /post/create

    # url(r'^(?P<pk>\d+)/$', post_detail_view, name='detail'),
    url(r'^(?P<pk>\d+)/$', PostDetailView.as_view(), name='detail'), # /post/1/

    # url(r'^(?P<pk>\d+)/repost/$', RepostView.as_view(), name='detail'),  # /post/45/retweet/


    # url(r'^(?P<pk>\d+)/update/$', PostUpdateView.as_view(), name='update'), # /post/1/update/

    # url(r'^(?P<pk>\d+)/delete/$', PostDeleteView.as_view(), name='delete'), # /post/1/delete/

]