from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic import CreateView
from .models import LodgingOfferCarousel, EducationalOfferSlider
from .forms import LodgingOfferCarouselForm, EducationalOfferSliderForm
from django.core.urlresolvers import reverse
from django.utils import timezone

from hostayni.mixins import UserProfileDataMixin
# Create your views here.


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


class EducationalOfferSliderCreateView(SuccessMessageMixin, LoginRequiredMixin, UserProfileDataMixin, CreateView):
    model = EducationalOfferSlider
    form_class = EducationalOfferSliderForm
    success_message = "La imagen ha sido adicionada al carrusel de la página de inicio"

    #def get_success_url(self):
    #    return reverse("carousels:lodging-offers-slider",)

    def form_valid(self, form):
        form.save(commit=False)
        form.instance.user = self.request.user
        form.instance.timestamp = timezone.now()
        form.save()
        return super(EducationalOfferSliderCreateView, self).form_valid(form)