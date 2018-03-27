from django.http import Http404
from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic import CreateView, UpdateView
from .models import (LodgingOfferCarousel, EducationalOfferCarousel, HomeCarousel, EntrepreneurshipOfferCarousel,
                    DailyLifeOfferCarousel)
from .forms import (LodgingOfferCarouselForm, EducationalOfferCarouselForm,
                    HomeCarouselForm, EntrepreneurshipOfferCarouselForm, DailyLifeOfferCarouselForm)
from django.core.urlresolvers import reverse
from django.utils import timezone

from hostayni.mixins import UserProfileDataMixin
# Create your views here.


class HomeCarouselCreateView(SuccessMessageMixin, LoginRequiredMixin, UserProfileDataMixin, CreateView):
    model = HomeCarousel
    form_class = HomeCarouselForm
    success_message = "La imagen ha sido adicionada al carrusel de la página de inicio"

    #def get_success_url(self):
    #    return reverse("carousels:home-slider",)

    def form_valid(self, form):
        form.save(commit=False)
        form.instance.user = self.request.user
        form.instance.timestamp = timezone.now()
        form.save()
        return super(HomeCarouselCreateView, self).form_valid(form)


class HomeSliderUpdateView(LoginRequiredMixin, SuccessMessageMixin, UserProfileDataMixin, UpdateView):
    form_class = HomeCarouselForm
    model = HomeCarousel
    success_message = "Imagen actualizada"

    # Permiso para que solo el dueño pueda editarla
    def get_object(self, queryset=None):
        """ Hook to ensure object is owned by request.user. """
        obj = super(HomeSliderUpdateView, self).get_object()
        # print(obj.user)
        if not obj.user == self.request.user:
            raise Http404
        return obj


class LodgingOfferCarouselCreateView(SuccessMessageMixin, LoginRequiredMixin, UserProfileDataMixin, CreateView):
    model = LodgingOfferCarousel
    form_class = LodgingOfferCarouselForm
    success_message = "La imagen ha sido adicionada al carrusel de la página de inicio"

    #def get_success_url(self):
    #    return reverse("carousels:lodging-offers-slider",)

    def form_valid(self, form):
        form.save(commit=False)
        form.instance.user = self.request.user
        form.instance.timestamp = timezone.now()
        form.save()
        return super(LodgingOfferCarouselCreateView, self).form_valid(form)


class EducationalOfferCarouselCreateView(SuccessMessageMixin, LoginRequiredMixin, UserProfileDataMixin, CreateView):
    model = EducationalOfferCarousel
    form_class = EducationalOfferCarouselForm
    success_message = "La imagen ha sido adicionada al carrusel de la página de inicio"

    #def get_success_url(self):
    #    return reverse("carousels:lodging-offers-slider",)

    def form_valid(self, form):
        form.save(commit=False)
        form.instance.user = self.request.user
        form.instance.timestamp = timezone.now()
        form.save()
        return super(EducationalOfferCarouselCreateView, self).form_valid(form)


class EntrepreneurshipOfferCarouselCreateView(SuccessMessageMixin, LoginRequiredMixin, UserProfileDataMixin, CreateView):
    model = EntrepreneurshipOfferCarousel
    form_class = EntrepreneurshipOfferCarouselForm
    success_message = "La imagen ha sido adicionada al carrusel de la página de inicio"

    #def get_success_url(self):
    #    return reverse("carousels:lodging-offers-slider",)

    def form_valid(self, form):
        form.save(commit=False)
        form.instance.user = self.request.user
        form.instance.timestamp = timezone.now()
        form.save()
        return super(EntrepreneurshipOfferCarouselCreateView, self).form_valid(form)


class DailyLifeOfferCarouselCreateView(SuccessMessageMixin, LoginRequiredMixin, UserProfileDataMixin, CreateView):
    model = DailyLifeOfferCarousel
    form_class = DailyLifeOfferCarouselForm
    success_message = "La imagen ha sido adicionada al carrusel de la página de inicio"

    #def get_success_url(self):
    #    return reverse("carousels:lodging-offers-slider",)

    def form_valid(self, form):
        form.save(commit=False)
        form.instance.user = self.request.user
        form.instance.timestamp = timezone.now()
        form.save()
        return super(DailyLifeOfferCarouselCreateView, self).form_valid(form)