from __future__ import unicode_literals
from django.shortcuts import render
from django.views.generic.edit import (CreateView, UpdateView,)
from django.views.generic.detail import DetailView
from django.contrib.messages.views import SuccessMessageMixin
from hostayni.mixins import UserProfileDataMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import EntrepreneurshipOffer
from .forms import EntrepreneurshipOfferForm
from django.utils import timezone


# Create your views here.


class EntrepreneurshipOfferCreateView(SuccessMessageMixin, LoginRequiredMixin, UserProfileDataMixin, CreateView):
    model = EntrepreneurshipOffer
    form_class = EntrepreneurshipOfferForm
    success_message = "Tu oferta de emprendiemiento fue creada con éxito. " \
                      "A continuación agrega más imágenes para generar " \
                      "mayor interés en los usuarios"

    def form_valid(self, form):
        form.save(commit=False)
        form.instance.created_by = self.request.user
        form.instance.created = timezone.now()
        form.save()
        return super(EntrepreneurshipOfferCreateView, self).form_valid(form)


class EntrepreneurshipOfferDetailView(SuccessMessageMixin, UserProfileDataMixin, LoginRequiredMixin, DetailView):
    model = EntrepreneurshipOffer
    template_name = 'entrepreneurship/detail.html'
    context_object_name = 'entrepreneurshipdetail'

    def get_context_data(self, **kwargs):
        context = super(EntrepreneurshipOfferDetailView, self).get_context_data(**kwargs)
        user = self.request.user


        # Capturamos quien creo la oferta, y su titulo de anuncio
        offer_owner = self.get_object().created_by.get_long_name()
        offer_owner_company = self.get_object().created_by.get_enterprise_name
        offer_owner_email = self.get_object().created_by.email
        offer_title = self.get_object().ad_title

        # Capturamos los datos de quien esta interesado en la oferta
        interested_email = user.email
        interested_username = user.username
        interested_full_name = user.get_long_name()


        offer_url = self.request.get_full_path

        # We get the images of LodgingOffer - LodgingOfferImages model
        entrepreneurship_offer = EntrepreneurshipOffer.objects.get(slug=self.kwargs.get('slug'))
        # We get images via related_name of lodging_offer pk in LodgingOfferImage model
        uploaded = entrepreneurship_offer.entrepreneurshipofferimage.all()

        # We send the contexts
        context['uploads'] = uploaded
        context['offer_owner_email'] = offer_owner_email
        context['offer_owner'] = offer_owner
        context['offer_owner_company'] = offer_owner_company
        context['offer_title'] = offer_title

        context['interested_email'] = interested_email
        context['interested_username'] = interested_username
        context['interested_full_name'] = interested_full_name

        context['offer_url'] = offer_url

        return context
