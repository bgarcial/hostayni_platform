from django.conf.urls import url
from hostayni.views import HomeSliderCreateView
from carousel_offers.views import LodgingOfferCarouselCreateView, EducationalOfferSliderCreateView

urlpatterns = [
    url(r'^home-slider/add/$', HomeSliderCreateView.as_view(), name='home-slider'),
    url(r'^lodging-offers-slider/add/$', LodgingOfferCarouselCreateView.as_view(),
        name='lodging-offers-slider'),
    url(r'^educational-offers-slider/add/$', EducationalOfferSliderCreateView.as_view(),
        name='educational-offers-slider'),
]