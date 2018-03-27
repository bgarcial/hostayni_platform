from django.conf.urls import url
from carousel_offers.views import (HomeCarouselCreateView, LodgingOfferCarouselCreateView, EducationalOfferCarouselCreateView,
                                    EntrepreneurshipOfferCarouselCreateView, DailyLifeOfferCarouselCreateView)

urlpatterns = [
    url(r'^home-slider/add/$', HomeCarouselCreateView.as_view(), name='home-slider'),

    url(r'^lodging-offers-slider/add/$', LodgingOfferCarouselCreateView.as_view(),
        name='lodging-offers-slider'),

    url(r'^educational-offers-slider/add/$', EducationalOfferCarouselCreateView.as_view(),
        name='educational-offers-slider'),

    url(r'^entrepreneurship-offers-slider/add/$', EntrepreneurshipOfferCarouselCreateView.as_view(),
        name='entrepreneurship-offers-slider'),

    url(r'^daily-life-offers-slider/add/$', DailyLifeOfferCarouselCreateView.as_view(),
        name='daily-life-offers-slider'),
]
