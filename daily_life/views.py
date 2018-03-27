from __future__ import unicode_literals
from django.shortcuts import render

from django.views.generic.edit import (CreateView, UpdateView,)
from django.views.generic.detail import DetailView
from django.views.generic import DeleteView, ListView
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils import timezone
from django.http import Http404, HttpResponseNotModified
from django.core.urlresolvers import reverse_lazy, reverse

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


class DailyLifeOfferDetailView(SuccessMessageMixin, UserProfileDataMixin, LoginRequiredMixin, DetailView):
    model = DailyLifeOffer
    template_name = 'daily_life/detail.html'
    context_object_name = 'dailylife'

    def get_context_data(self, **kwargs):
        context = super(DailyLifeOfferDetailView, self).get_context_data(**kwargs)
        user = self.request.user

        # Capturamos quien creo la oferta, y su titulo de anuncio

        offer_owner = self.get_object().created_by.get_long_name()

        offer_owner_company = self.get_object().created_by.get_enterprise_name

        offer_owner_username = self.get_object().created_by.username

        offer_owner_email = self.get_object().created_by.email

        offer_title = self.get_object().ad_title

        # Capturamos los datos de quien esta interesado en la oferta
        interested_email = user.email

        interested_username = user.username

        interested_full_name = user.get_long_name()

        offer_url = self.request.get_full_path
        # print(offer_url)

        # We get the images of DailyLifeOffer - DailyLifeOfferImages model
        daily_life_offer = DailyLifeOffer.objects.get(slug=self.kwargs.get('slug'))

        # We get images via related_name of lodging_offer pk in LodgingOfferImage model
        uploaded = daily_life_offer.dailylifeofferimage.all()

        # We send the contexts
        context['uploads'] = uploaded
        context['offer_owner_username'] = offer_owner_username
        context['offer_owner_email'] = offer_owner_email
        context['offer_owner'] = offer_owner
        # context['offer_owner_company'] = offer_owner_company
        context['offer_title'] = offer_title

        context['interested_email'] = interested_email
        context['interested_username'] = interested_username
        context['interested_full_name'] = interested_full_name

        context['offer_url'] = offer_url

        return context


class DailyLifeOfferUpdateView(SuccessMessageMixin, UserProfileDataMixin, LoginRequiredMixin, UpdateView):
    model = DailyLifeOffer
    form_class = DailyLifeOfferForm
    success_message = "Oferta de vida diaria actualizada con éxito"
    # template_name = 'entrepreneruship/delete.html'

    def get_context_data(self, **kwargs):
        context = super(DailyLifeOfferUpdateView, self).get_context_data(**kwargs)
        # user = self.request.user
        return context

    # Permiso para que solo el dueño pueda editarla
    def get_object(self, queryset=None):
        """ Hook to ensure object is owned by request.user. """
        obj = super(DailyLifeOfferUpdateView, self).get_object()
        if not obj.created_by == self.request.user:
            raise Http404
        return obj


class DailyLifeOfferDeleteView(SuccessMessageMixin, UserProfileDataMixin, LoginRequiredMixin, DeleteView):
    model = DailyLifeOffer

    success_url = reverse_lazy("articles:article_list")
    # context_object_name = 'lodgingofferdelete'
    success_message = "Oferta de vida diaria eliminada con éxito"

    """
    def get_success_url(self):
        entrepreneurship_offer = self.get_object()
        #print(entrepreneurship_offer)
        return reverse_lazy("offer:list", kwargs={'created_by': entrepreneurship_offer.created_by.username})
    """

    def get_object(self, queryset=None):
        """ Hook to ensure object is owned by request.user. """
        obj = super(DailyLifeOfferDeleteView, self).get_object()
        if not obj.created_by == self.request.user:
            raise Http404
        return obj
