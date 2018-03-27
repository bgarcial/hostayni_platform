from __future__ import unicode_literals
from django.shortcuts import render

from django.views.generic.edit import (CreateView, UpdateView,)
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils import timezone

from hostayni.mixins import UserProfileDataMixin
from .models import DailyLifeOffer
from .forms import DailyLifeOfferForm

# Create your views here.


class DailyLifeOfferCreateView(SuccessMessageMixin, LoginRequiredMixin, UserProfileDataMixin, CreateView):
    model = DailyLifeOffer
    form_class = DailyLifeOfferForm
    success_message = "Tu oferta de emprendiemiento fue creada con éxito. " \
                      "A continuación agrega más imágenes para generar " \
                      "mayor interés en los usuarios"

    def form_valid(self, form):
        form.save(commit=False)
        form.instance.created_by = self.request.user
        form.instance.created = timezone.now()
        form.save()
        return super(DailyLifeOfferCreateView, self).form_valid(form)

