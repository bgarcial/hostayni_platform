from django.conf.urls import url


from .views import DailyLifeOfferCreateView


urlpatterns = [

    # Create Daily life Offer
    url(r'^new/$',
        DailyLifeOfferCreateView.as_view(),
        name='create'),
]