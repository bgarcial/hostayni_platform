from django.conf.urls import url
from .views import (EntrepreneurshipOfferCreateView, EntrepreneurshipOfferDetailView,
                    EntrepreneurshipOfferUpdateView, EntrepreneurshipOfferDeleteView,
                    entrepreneurship_offers_by_user, EntrepreneurshipOffersByUser)

urlpatterns = [

    # Create Entrepreneurship Offer
    url(r'^new/$',
        EntrepreneurshipOfferCreateView.as_view(),
        name='create'),

    # Detail of a Entrepreneurship Offer
    url(r"^(?P<slug>[\w-]+)/$",
        EntrepreneurshipOfferDetailView.as_view(),
        name='detail'),

    # Edit Entrepreneurship Offer
    url(r"^(?P<slug>[\w-]+)/edit/$",
        EntrepreneurshipOfferUpdateView.as_view(),
        name='edit'),

    # Delete of a Entrepreneurship Offer
    url(r"^(?P<slug>[\w-]+)/delete/$",
        EntrepreneurshipOfferDeleteView.as_view(),
        name='delete'),

    # List Entrepreneurship Offer's user
    url(r'^by/u/(?P<username>[-\w]+)/$',
        EntrepreneurshipOffersByUser.as_view(),
        name='list'),
    ]

