from __future__ import unicode_literals
from django.shortcuts import render, redirect

from django.views.generic.edit import (CreateView, UpdateView,)
from django.views.generic.detail import DetailView
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils import timezone
from hostayni.mixins import UserProfileDataMixin
from .models import AyniOffer
from .forms import AyniOfferForm

# Create your views here.


class AyniOfferCreateView(SuccessMessageMixin, LoginRequiredMixin, UserProfileDataMixin, CreateView):
    model = AyniOffer
    form_class = AyniOfferForm
    success_message = "Tu oferta de emprendiemiento fue creada con éxito. " \
                      "A continuación agrega más imágenes para generar " \
                      "mayor interés en los usuarios"

    def form_valid(self, form):
        form.save(commit=False)
        form.instance.created_by = self.request.user
        form.instance.created = timezone.now()
        form.save()
        return super(AyniOfferCreateView, self).form_valid(form)


class AyniOfferDetailView(SuccessMessageMixin, UserProfileDataMixin, LoginRequiredMixin, DetailView):
    model = AyniOffer
    template_name = 'ayni/detail.html'
    context_object_name = 'dailylife'

    def get_context_data(self, **kwargs):
        context = super(AyniOfferDetailView, self).get_context_data(**kwargs)
        user = self.request.user

        # Capturamos quien creo la oferta, y su titulo de anuncio

        offer_owner = self.get_object().created_by.get_long_name()
        print("Dueño de la oferta", offer_owner)

        offer_owner_company = self.get_object().created_by.enterprise_name
        print("Dueño por si es una compania", offer_owner_company)

        offer_owner_username = self.get_object().created_by.username
        print("Username del dueño de oferta", offer_owner_username)

        offer_owner_email = self.get_object().created_by.email
        print("Emai dueño oferta", offer_owner_email)

        offer_title = self.get_object().ad_title
        print("Titulo ofeta", offer_title)

        # Capturamos los datos de quien esta interesado en la oferta
        interested_email = user.email
        print(interested_email)

        interested_username = user.username
        print(interested_username)

        interested_full_name = user.get_long_name()
        print(interested_full_name)

        offer_url = self.request.get_full_path
        print(offer_url)

        # We get the images of AyniOffer - AyniOfferImages model
        ayni_offer = AyniOffer.objects.get(slug=self.kwargs.get('slug'))

        # We get images via related_name of ayni_offer pk in AyniOfferImage model
        uploaded = ayni_offer.ayniofferimage.all()

        # We send the contexts
        context['uploads'] = uploaded
        context['offer_owner_username'] = offer_owner_username
        context['offer_owner_email'] = offer_owner_email
        context['offer_owner'] = offer_owner
        context['offer_owner_company'] = offer_owner_company
        # context['offer_owner_company'] = offer_owner_company
        context['offer_title'] = offer_title

        context['interested_email'] = interested_email
        context['interested_username'] = interested_username
        context['interested_full_name'] = interested_full_name

        context['offer_url'] = offer_url

        return context