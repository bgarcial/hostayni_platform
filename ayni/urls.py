from django.conf.urls import url
from .views import (AyniOfferCreateView, AyniOfferDetailView)

urlpatterns = [

    # Create Ayni Offer
    url(r'^new/$',
        AyniOfferCreateView.as_view(),
        name='create'),

    # Detail of a Ayni Offer
    url(r"^(?P<slug>[\w-]+)/$",
        AyniOfferDetailView.as_view(),
        name='detail'),
]