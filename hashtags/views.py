from django.views import View
from django.shortcuts import render
from hostayni.mixins import UserProfileDataMixin

from .models import HashTag


class HashTagView(UserProfileDataMixin, View):
    def get(self, request, hashtag, *args, **kwargs):
        obj, created = HashTag.objects.get_or_create(tag=hashtag)

        return render(request, 'hashtags/tag_view.html', {"obj": obj})