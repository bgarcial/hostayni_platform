from django.conf.urls import url

from .views import (HostingOfferCreateView, HostingOfferUpdateView,
                    StudyOfferCreateView, StudyOffertDetailView,
                    HostingOfferDetailView, lodging_offers_by_user,
                    studies_offers_by_user, StudyOfferUpdateView,
                    LodgingOfferSearch, StudiesOffertSearch,
                    HostingOfferDeleteView, StudyOfferDeleteView,
                    LodgingOffersByUser, LodgingOfferAjax)


urlpatterns = [

    # ----------------------Hosting Offers-------------------

    # GET lodging-offers from ajax
    url(r'^ofertas-get-ajax/$',
        LodgingOfferAjax.as_view(),
        name='lodging-ajax-offers'
    ),

    # Create Hosting Offer
    url(r'^lodging-offer/new/$',
        HostingOfferCreateView.as_view(),
        name='hosting-host'
    ),

    # List Hosting Offers
    url(r'^lodging-offers/by/u/@(?P<email>[-\w]+)/$',
        lodging_offers_by_user,
        name='list'
    ),


    url(r'^ofertas/by/u/@(?P<username>[-\w]+)/$',
       LodgingOffersByUser.as_view(),
        name='list2'
    ),


    # Edit Hosting offer
    url(r"^lodging-offer/(?P<pk>\d+)/edit/$",
        HostingOfferUpdateView.as_view(),
        name='edit-lodging-offer'
    ),

    # Delete of a Hosting Offer
    url(r"^lodging-offer/(?P<pk>\d+)/delete/$",
        HostingOfferDeleteView.as_view(),
        name='delete-lodging-offer'
    ),

    # Detail a Hosting Offer
    url(r"^lodging-offer/(?P<pk>\d+)/$",
        HostingOfferDetailView.as_view(),
        name='detail'
    ),




    # Search Hosting Offer
    url(r'^lodging-offer/search/$',
        LodgingOfferSearch.as_view(),
        name='hostingoffer-search'
    ),


    # ----------------------Study Offers-------------------

    # Create Study Host Offer
    url(r'^studies-offer/new',
        StudyOfferCreateView.as_view(),
        name='study-host'
    ),

    # List Study Host Offers
    url(r'^studies-offers/by/u/@(?P<email>[-\w]+)/',
        studies_offers_by_user,
        name='studiesofferlist'
    ),

    # Edit Studies offer
    url(r"^study-offer/(?P<pk>\d+)/edit/$",
        StudyOfferUpdateView.as_view(),
        name='edit-study-offer'
    ),



    # Delete of a Hosting Offer
    url(r"^study-offer/(?P<pk>\d+)/delete/$",
        StudyOfferDeleteView.as_view(),
        name='delete-study-offer'
    ),

    #Detail of Studies Offert
    url(r'^study-offer/(?P<pk>\d+)/',
        StudyOffertDetailView.as_view(),
        name='studyoffertdetail'
    ),

    # Search Studies Offer
    url(r'^study-offer/search/$',
        StudiesOffertSearch.as_view(),
        name='studyoffer-search'
    ),





]