from __future__ import unicode_literals

from django.contrib.auth import get_user_model
from django.views import generic
from django.core.urlresolvers import reverse_lazy, reverse
from django.contrib.auth import login, logout, authenticate

from django.shortcuts import render

from .forms import (
        StudentProfileForm, ExecutiveProfileForm,
        ProfessorProfileForm, UserCreateForm, UserUpdateForm,
        StudyHostProfileForm, HostingHostProfileForm, )
from .models import (
        StudentProfile, ProfessorProfile,
        ExecutiveProfile, User, UserProfile
        )

User = get_user_model()


class LogoutView(generic.RedirectView):
    # Redirect back to article list
    url = reverse_lazy('articles:article_list')

    # se dispara cuando entra el request entrante
    def get(self, request, *args, **kwargs):
        # Llamamos a logout with the request
        logout(request)
        return super().get(request, *args, **kwargs)


class SignUpView(generic.CreateView):
    form_class = UserCreateForm
    success_url = reverse_lazy("login")
    template_name = "accounts/signup.html"