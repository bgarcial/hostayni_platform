from django.conf.urls import url

# Importamos la vista serializable de Posts de la cual se consumen los posts creados
from posts.api.views import (
    PostListAPIView,

    )


urlpatterns = [
    # URL para los posts que un usuario ha creado o reposteado
    # url(r'^(?P<email>[\w.@+-]+)/post/$', PostListAPIView.as_view(), name='list'), #/api/username/post/
    url(r'^(?P<username>[\w.\-]+)/post/$', PostListAPIView.as_view(), name='list'), #/api/username/post/
]