from django.db.models import Q
# from django.shortcuts import get_object_or_404
from rest_framework import generics
from rest_framework import permissions
from rest_framework.views import APIView
from rest_framework.response import Response

from posts.models import Post
from .serializers import PostModelSerializer
from .pagination import StandardResultsPagination

class LikeToggleAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, pk, format=None):
        post_qs = Post.objects.filter(pk=pk)
        message = "Not allowed"

        if request.user.is_authenticated():

            # Llamamos al PostManager y le pasamos el user que hace el like con like_toggle
            is_liked = Post.objects.like_toggle(request.user, post_qs.first())
            return Response({"liked": is_liked})
        return Response({"message": message}, status=400)

    # http://www.django-rest-framework.org/api-guide/views/
    # Managing retweets not same in 1 day

class RepostAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, pk, format=None):
        post_qs = Post.objects.filter(pk=pk)
        message = "Not allowed"
        # Si el post existe y es solo uno
        if post_qs.exists() and post_qs.count() == 1:
            # if request.user.is_authenticated():
            # Llamamos al PostManager y le pasamos el user que hace el repost y el post
            new_post = Post.objects.repost(request.user, post_qs.first())

            if new_post is not None:
                # Serializamos y desplegamos el resultado de la consulta que es el post reposteado
                # como respuesta retornada
                data = PostModelSerializer(new_post).data
                return Response(data)
            message = "Cannot repost the same in 1 day"
        return Response({"message": message}, status=400)


# http://www.django-rest-framework.org/api-guide/generic-views/#createapiview

class PostCreateAPIView(generics.CreateAPIView):
    serializer_class = PostModelSerializer
    # Solicita Credenciales de autenticacion
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


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


# ApiView para encontrar post de cualquier persona

class SearchPostAPIView(generics.ListAPIView):
    queryset = Post.objects.all().order_by('-timestamp')
    serializer_class = PostModelSerializer
    pagination_class = StandardResultsPagination

    def get_serializer_context(self, *args, **kwargs):
        context = super(SearchPostAPIView, self).get_serializer_context(*args, **kwargs)
        context['request'] = self.request
        return context

    def get_queryset(self, *args, **kwargs):
        # Le decimos que para el mismo queryset global definido
        qs = self.queryset
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
