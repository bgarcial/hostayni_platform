from django.conf.urls import url


from .views import (DailyLifeOfferCreateView, DailyLifeOfferDetailView, DailyLifeOfferUpdateView,
                    DailyLifeOfferDeleteView)


urlpatterns = [

    # Create Daily life Offer
    url(r'^new/$',
        DailyLifeOfferCreateView.as_view(),
        name='create'),

    # Detail of a Daily life Offer
    url(r"^(?P<slug>[\w-]+)/$",
        DailyLifeOfferDetailView.as_view(),
        name='detail'),

    # Edit Daily life Offer
    url(r"^(?P<slug>[\w-]+)/edit/$",
        DailyLifeOfferUpdateView.as_view(),
        name='edit'),

    # Delete of a Entrepreneurship Offer
    url(r"^(?P<slug>[\w-]+)/delete/$",
        DailyLifeOfferDeleteView.as_view(),
        name='delete'),
]