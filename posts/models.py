import re

from django.db import models
from django.db.models.signals import post_save
from django.conf import settings
from django.urls import reverse
from .validators import validate_content
from django.utils import timezone


# Model Manager

class PostManager(models.Manager):

    def repost(self, user, parent_obj):
        if parent_obj.parent:
            # Original parent
            og_parent = parent_obj.parent
        else:
            og_parent = parent_obj

        # FIltre los posts que tengan post padre
        qs = self.get_queryset().filter(
                user=user, parent=og_parent
                ).filter(
                    timestamp__year=timezone.now().year,
                    timestamp__month=timezone.now().month,
                    timestamp__day=timezone.now().day,
                    reply=False,

                )
        if qs.exists():
            return None
        # else:


        obj = self.model(
            parent=og_parent,
            user=user,
            content=parent_obj.content,
        )
        obj.save()
        return obj

    def like_toggle(self, user, post_obj):
        # If user is in users que dieron like
        if user in post_obj.liked.all():
            # Not enabled to make Like
            is_liked = False
            post_obj.liked.remove(user)
        else:
            # Post Enabled to like
            is_liked = True
            post_obj.liked.add(user)
        return is_liked


class Post(models.Model):
    parent = models.ForeignKey("self", blank=True, null=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, default=1,)
    content = models.TextField(validators=[validate_content])
    # fix max_length?

    liked = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, related_name='liked')
    reply = models.BooleanField(verbose_name='Is a reply?', default=False)
    updated = models.DateTimeField(auto_now=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    objects = PostManager()

    def __str__(self):
        return str(self.content)

    def get_absolute_url(self):
        return reverse('post:detail', kwargs={"pk":self.pk})

    class Meta:
        ordering = ['-timestamp']

    # Obteniendo el post padre
    def get_parent(self):
        the_parent = self
        # Si existe un post padre
        if self.parent:
            # Asignemoslo a the_parent
            the_parent = self.parent
        return the_parent

    # Para ver las respuestas que puede tener un post
    def get_children(self):
        # Capturamos el post padre
        parent = self.get_parent()
        # COnsultamos los posts que tengan ese padre
        qs = Post.objects.filter(parent=parent)
        qs_parent = Post.objects.filter(pk=parent.pk)
        return (qs | qs_parent)

    # Validation
    """
    def clean(self, *args, **kwargs):
        content = self.content
        if content == 'abc':
            raise ValidationError("Content cannot be ABC")
        return super(Post, self).clean(*args, **kwargs)
    """

# post_save
def post_save_receiver(sender, instance, created, *args, **kwargs):
    # Si fue un post creado y no reposteado
    if created and not instance.parent:
        # notify a user
        user_regex = r'@(?P<email>[\w.@+-]+)'
        # match
        emails = re.findall(user_regex, instance.content)
        # if emails:
            # print(emails)
            # email = m.group("email")
            # print(email)

        # Enviar notificacion al usuario aqui
        # Agregar esto de hashtags mas tarde

        '''
        # Agrupamos todos los #hashtags que se pongan en un post y los
        # ponemos en una lista en parsed_hashtags en signals.py
        hash_regex = r'#(?P<hashtag>[\w\d-]+)'
        hashtags = re.findall(hash_regex, instance.content)
        # if hashtags:
            # print(hashtags)
            #hashtag = m.group("hashtag")
            #print(hashtag)

        # La propia clase Post
        parsed_hashtags.send(sender=instance.__class__, hashtag_list=hashtags)
        # Enviar hashtag signal al usuario aqui
        '''

# post_save.connect(post_save_receiver, sender=Post)
