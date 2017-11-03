from django.conf.urls import url
from .views import (
    LikeToggleAPIView,
    # RepostAPIView,
    PostListAPIView,
    PostCreateAPIView,
    PostDetailAPIView,

    )


urlpatterns = [
    url(r'^$', PostListAPIView.as_view(), name='list'), #/api/post/
    url(r'^create/$', PostCreateAPIView.as_view(), name='create'), #/api/post/create
    url(r'^(?P<pk>\d+)/$', PostDetailAPIView.as_view(), name='detail'), #/api/post/id/
    url(r'^(?P<pk>\d+)/like/$', LikeToggleAPIView.as_view(), name='like-toggle'), #/api/post/id/like/
    # url(r'^(?P<pk>\d+)/repost/$', RepostAPIView.as_view(), name='repost'), #/api/post/id/repost/


]