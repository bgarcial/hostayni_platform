from django.conf.urls import url
from carousel_offers.views import HomeCarouselCreateView
from carousel_offers.views import (LodgingOfferCarouselCreateView, EducationalOfferCarouselCreateView,
                                    EntrepreneurshipOfferCarouselCreateView)

urlpatterns = [
    url(r'^home-slider/add/$', HomeCarouselCreateView.as_view(), name='home-slider'),

    url(r'^lodging-offers-slider/add/$', LodgingOfferCarouselCreateView.as_view(),
        name='lodging-offers-slider'),

    url(r'^educational-offers-slider/add/$', EducationalOfferCarouselCreateView.as_view(),
        name='educational-offers-slider'),

    url(r'^entrepreneurship-offers-slider/add/$', EntrepreneurshipOfferCarouselCreateView.as_view(),
        name='entrepreneurship-offers-slider'),
]
