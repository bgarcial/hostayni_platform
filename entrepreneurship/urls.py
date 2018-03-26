from django.conf.urls import url
from .views import EntrepreneurshipOfferCreateView, EntrepreneurshipOfferDetailView

urlpatterns = [

    # Create Entrepreneurship Offer
    url(r'^entrepreneurship/new/$',
        EntrepreneurshipOfferCreateView.as_view(),
        name='create'),

    # Detail of a Entrepreneurship Offer
    url(r"^entrepreneurship/(?P<slug>[\w-]+)/$",
        EntrepreneurshipOfferDetailView.as_view(),
        name='detail'),
    ]