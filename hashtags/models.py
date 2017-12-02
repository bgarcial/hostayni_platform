from django.db import models
from django.urls import reverse_lazy
from posts.models import Post
from .signals import parsed_hashtags


class HashTag(models.Model):
    tag = models.CharField(max_length=120)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.tag

    def get_absolute_url(self):
        return reverse_lazy("hashtag", kwargs={"hashtag":self.tag})

    def get_posts(self):
        return Post.objects.filter(content__contains="#" + self.tag)

def parsed_hashtags_receiver(sender, hashtag_list, *args, **kwargs):
    # print(args)
    # print(kwargs)
    if len(hashtag_list) > 0:
        for tag_var in hashtag_list:
            new_tag, created = HashTag.objects.get_or_create(tag=tag_var)


parsed_hashtags.connect(parsed_hashtags_receiver)