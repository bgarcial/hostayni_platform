from __future__ import unicode_literals

from django.http import Http404
from django.shortcuts import render
from django.views.generic.edit import (CreateView, UpdateView,)
from django.views.generic.detail import DetailView
from django.views.generic import DeleteView, ListView
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils import timezone
from django.core.urlresolvers import reverse_lazy, reverse

from .models import EntrepreneurshipOffer
from .forms import EntrepreneurshipOfferForm
from hostayni.mixins import UserProfileDataMixin

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
    # context_object_name = 'entrepreneurshipdetail'

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


class EntrepreneurshipOfferUpdateView(SuccessMessageMixin, UserProfileDataMixin, LoginRequiredMixin, UpdateView):
    model = EntrepreneurshipOffer
    form_class = EntrepreneurshipOfferForm
    success_message = "Oferta de emprendimiento actualizada con éxito"
    # template_name = 'entrepreneruship/delete.html'

    def get_context_data(self, **kwargs):
        context = super(EntrepreneurshipOfferUpdateView, self).get_context_data(**kwargs)
        # user = self.request.user
        return context

    # Permiso para que solo el dueño pueda editarla
    def get_object(self, queryset=None):
        """ Hook to ensure object is owned by request.user. """
        obj = super(EntrepreneurshipOfferUpdateView, self).get_object()
        if not obj.created_by == self.request.user:
            raise Http404
        return obj


class EntrepreneurshipOfferDeleteView(SuccessMessageMixin, UserProfileDataMixin, LoginRequiredMixin, DeleteView):
    model = EntrepreneurshipOffer

    success_url = reverse_lazy("articles:article_list")
    # context_object_name = 'lodgingofferdelete'
    success_message = "Oferta de alojamiento eliminada con éxito"

    """
    def get_success_url(self):
        entrepreneurship_offer = self.get_object()
        #print(entrepreneurship_offer)
        return reverse_lazy("offer:list", kwargs={'created_by': entrepreneurship_offer.created_by.username})
    """

    def get_object(self, queryset=None):
        """ Hook to ensure object is owned by request.user. """
        obj = super(EntrepreneurshipOfferDeleteView, self).get_object()
        if not obj.created_by == self.request.user:
            raise Http404
        return obj

    def get_context_data(self, **kwargs):
        context = super(EntrepreneurshipOfferDeleteView, self).get_context_data(**kwargs)
        return context


def entrepreneurship_offers_by_user(request, username):
    user = request.user
    profile = user.profile
    entrepreneurship_offers = EntrepreneurshipOffer.objects.filter(created_by__username=user.username)

    return render(
        request,
        'entrepreneurship/my_entrepreneurship_offer_list.html',
        {'entrepreneurship_offers': entrepreneurship_offers,
        'userprofile': profile}
    )


class EntrepreneurshipOffersByUser(LoginRequiredMixin, UserProfileDataMixin, ListView):
    template_name = 'entrepreneurship/my_entrepreneurship_offer_list.html'

    def get_queryset(self, *args, **kwargs):
        user = self.request.user
        queryset_list = EntrepreneurshipOffer.objects.filter(created_by__username=user.username)
        return queryset_list

    def get_context_data(self, **kwargs):
        context = super(EntrepreneurshipOffersByUser, self).get_context_data(**kwargs)
        user = self.request.user
        entrepreneurship_offers = EntrepreneurshipOffer.objects.filter(created_by__username=user.username)
        context['offers_by_user'] = entrepreneurship_offers

        #if user.is_authenticated():
        #    context['userprofile'] = user.profile
        return context
