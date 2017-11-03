from django.db.models import Q
# from django.shortcuts import get_object_or_404
from rest_framework import generics
from rest_framework import permissions
from rest_framework.views import APIView
from rest_framework.response import Response

from posts.models import Post
from .serializers import PostModelSerializer
from .pagination import StandardResultsPagination


class PostDetailAPIView(generics.ListAPIView):
    queryset = Post.objects.all()
    serializer_class = PostModelSerializer
    pagination_class = StandardResultsPagination
    # Cualquiera puede ver esta vista
    permission_classes = [permissions.AllowAny]

    # Para averiguar un hilo de posts, las respuestas a un post
    def get_queryset(self, *args, **kwargs):
        post_id = self.kwargs.get("pk")
        qs = Post.objects.filter(pk=post_id)
        # Si el post retornado existe y al contarlo es 1
        if qs.exists() and qs.count() == 1:
            parent_obj = qs.first()
            qs1 = parent_obj.get_children()
            qs = (qs | qs1).distinct().extra(select={"parent_id_null": 'parent_id IS NULL'})

        # Respuestas hijas y ordenandolas por orden de posteada teniendo
        # el post padre primero
        return qs.order_by("-parent_id_null", 'timestamp')


# http://www.django-rest-framework.org/api-guide/generic-views/#listapiview
# http://www.django-rest-framework.org/api-guide/pagination/

#Esta vista servira para listar los posts en el sistema y para listar
# los posts de un usuario en particular


# ApiView para encontrar post de quienes sig


class PostListAPIView(generics.ListAPIView):
    serializer_class = PostModelSerializer
    pagination_class = StandardResultsPagination

    # ****
    # Los posts seran mostrados depende del usuario que esta
    # actualmente logueado, por eso el get_serializer_context
    # para adicionar el usuario que hace el request /api/post,
    # al contexto y asi pasarlo
    # https://stackoverflow.com/questions/31038742/pass-request-context-to-serializer-from-viewset-in-django-rest-framework

    # Con get_serializer se pueden adicionar elementos al contexto en un APIView o ViewSet
    # https://stackoverflow.com/questions/38177270/where-does-the-self-get-serializer-method-come-from-in-the-django-rest-framework
    def get_serializer_context(self, *args, **kwargs):
        context = super(PostListAPIView, self).get_serializer_context(*args, **kwargs)
        context['request'] = self.request
        return context

    # ****

    '''
    def get_serializer_context(self):
        context = super(PostListAPIView, self).get_serializer_context()
        context = {'request': self.request.user,
                   'logged_In': self.request.user.is_authenticated()}
        return context
    '''
    def get_queryset(self, *args, **kwargs):
        # qs = Post.objects.all().order_by('-updated')

        # Capturamos el request de un usuario
        requested_user = self.kwargs.get("email")

        if requested_user:

            # Mostrando los posts de un usuaSrio en especial
            # Bind querysets https://www.udemy.com/tweetme-django/learn/v4/t/lecture/6134712?start=0
            # Para ver los posts mios y los que reposteo
            qs = Post.objects.filter(user__email=requested_user).order_by('-timestamp')
            # print(self.request.GET)
        else:
            im_following = self.request.user.profile.get_following() # none
            #qs = Post.objects.all().order_by('-timestamp')

            # Mostrando los posts de los usuarios que sigo
            # Bind querysets https://www.udemy.com/tweetme-django/learn/v4/t/lecture/6134712?start=0
            # Para ver los posts de los que sigo y los mios
            qs1 = Post.objects.filter(user__in=im_following)
            qs2 = Post.objects.filter(user = self.request.user)
            qs = (qs1 | qs2).distinct().order_by('-timestamp')
            # print(self.request.GET)

        query = self.request.GET.get("q", None)
        if query is not None:
            # qs = qs.filter(content__icontains=query)
            # Mirar esto
            # https://docs.djangoproject.com/en/1.11/topics/db/queries/#complex-lookups-with-q-objects
            qs = qs.filter(
                Q(content__icontains=query) |
                Q(user__email__icontains=query)
                )
        return qs
