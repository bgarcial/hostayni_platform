from django.db.models import Q
from rest_framework import generics
from rest_framework import permissions
from rest_framework.views import APIView
from rest_framework.response import Response

from posts.models import  Post
from posts.api.serializers import PostModelSerializer
from posts.api.pagination import StandardResultsPagination
from ..models import HashTag


class TagPostAPIView(generics.ListAPIView):
    queryset = Post.objects.all().order_by('-timestamp')
    serializer_class = PostModelSerializer
    pagination_class = StandardResultsPagination

    def get_serializer_context(self, *args, **kwargs):
        context = super(TagPostAPIView, self).get_serializer_context(*args, **kwargs)
        context['request'] = self.request
        return context

    def get_queryset(self, *args, **kwargs):
        hashtag = self.kwargs.get('hashtag')
        hashtag_obj = None
        try:
            hashtag_obj = HashTag.objects.get_or_create(tag=hashtag)[0]
        except:
            pass
        if hashtag_obj:
            qs = hashtag_obj.get_posts()
            query = self.request.GET.get("q", None)
            if query is not None:
                # qs = qs.filter(content__icontains=query)
                # Mirar esto
                # https://docs.djangoproject.com/en/1.11/topics/db/queries/#complex-lookups-with-q-objects
                # que busque por contenido y email un post de cualquier persona
                qs = qs.filter(
                    Q(content__icontains=query) |
                    Q(user__email__icontains=query)
                    )
            return qs
        return None
