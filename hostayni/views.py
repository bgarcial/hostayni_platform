# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth import get_user_model

from django.db.models import Q

from django.views.generic.base import TemplateView

from .mixins import UserProfileDataMixin

User = get_user_model()


class HomePageView(TemplateView):
    template_name = 'hostayni/home-bootstrap.html'

    def get_context_data(self, **kwargs):
        context = super(HomePageView, self).get_context_data(**kwargs)
        # messages.info(self.request, 'hello http://example.com')
        user = self.request.user
        #context['userprofile'] = user.profile
        if user.is_authenticated():
            context['userprofile'] = user.profile
        # else:
        return context


# Buscando Users en hostayni social

class SearchView(UserProfileDataMixin, TemplateView):

    def get(self, request, *args, **kwargs):
        query = request.GET.get("q")
        qs = None
        if query:
            qs = User.objects.filter(
                    Q(email__icontains=query)
                    # Aca podriamos buscar por cualquier atributo
                    # relacionado con el usuario o del usuario
                    # # https://docs.djangoproject.com/en/1.11/topics/db/queries/#complex-lookups-with-q-objects
                )
        context = {"users": qs}
        return render(request, "search.html", context)



def home(request):
    context = {}
    return render(request, 'hostayni/home.html', context)



def home_files(request, filename):
    return render(request, filename, {}, content_type="text/plain")