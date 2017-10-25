from django.conf.urls import url

from .views import (
    HostingOfferCreateView, HostingOfferUpdateView,
    StudyOfferCreateView, StudyOffertDetailView,
    HostingOfferDetailView, lodging_offers_by_user,
    studies_offers_by_user, StudyOfferUpdateView,
    LodgingOfferSearch, StudiesOffertSearch,
    HostingOfferDeleteView, StudyOfferDeleteView,
    LodgingOfferAjax, contact_owner_offer, contact_study_owner_offer,
    edit_study_offer_uploads, delete_upload_study_offer_image, StudyOfferImageUpdateView,
    edit_lodging_offer_uploads_image, LodgingOfferImageUpdateView,
    delete_lodging_offer_image,
)


urlpatterns = [

    # ----------------------Hosting Offers-------------------

    # GET lodging-offers from ajax
    url(r'^ofertas-get-ajax/$',
        LodgingOfferAjax.as_view(),
        name='lodging-ajax-offers'),

    # Create Lodging Offer
    url(r'^lodging-offer/new/$',
        HostingOfferCreateView.as_view(),
        name='hosting-host'),

    # List Lodging Offer's user
    url(r'^lodging-offers/by/u/@(?P<email>[-\w]+)/$',
        lodging_offers_by_user,
        name='list'),

    # Editando imagenes de ofertas de alojamiento
    url(r"^lodging-offer/edit/images/(?P<pk>\d+)/$",
        LodgingOfferImageUpdateView.as_view(),
        name='edit-lodging-offer-image'),

    # Edit Lodging offer
    url(r"^lodging-offer/(?P<slug>[\w-]+)/edit/$",
        HostingOfferUpdateView.as_view(),
        name='edit-lodging-offer'),


    # Delete of a Lodging Offer
    url(r"^lodging-offer/(?P<slug>[\w-]+)/delete/$",
        HostingOfferDeleteView.as_view(),
        name='delete-lodging-offer'),

    # Upload/View Lodging Offer images edit_lodging_offer_uploads_image
    url(r'^lodging-offer/(?P<slug>[-\w]+)/edit/images/$',
        edit_lodging_offer_uploads_image, name='edit_lodging_offer_uploads_image'),


    url(r'^lodging-offer/delete/images/(?P<id>[-\w]+)/$',
        delete_lodging_offer_image, name='delete-lodging-offer-image'),

    # Search Hosting Offer
    url(r'^lodging-offer/search/$',
        LodgingOfferSearch.as_view(),
        name='hostingoffer-search'),

    # Detail of a LodgingOffer
    url(r"^lodging-offer/(?P<slug>[\w-]+)/$",
        HostingOfferDetailView.as_view(),
        name='detail'),


    url(r'^contact-to-owner/(?P<lodging_offer_owner_full_name>[\w." "@+-]+)/(?P<lodging_offer_owner_email>[\w.@+-]+)/from/'
        r'(?P<user_interested_full_name>[\w." "@+-]+)/(?P<interested_email>[\w.@+-]+)/'
        r'(?P<lodging_offer_title>[\w." "@+-]+)/(?P<offer_url>[\w.@+-/]+)/$',
        contact_owner_offer,
        name='contact_owner_offer'),

    # ----------------------Study Offers-------------------

    # Create Study Host Offer
    url(r'^studies-offer/new',
        StudyOfferCreateView.as_view(),
        name='study-host'),

    # List Study Host Offers
    url(r'^studies-offers/by/u/@(?P<email>[-\w]+)/',
        studies_offers_by_user,
        name='studiesofferlist'),





    # Editando imagen de estudios
    url(r"^study-offer/edit/images/(?P<pk>\d+)/$",
        StudyOfferImageUpdateView.as_view(),
        name='edit-study-offer-image'),




    # Edit Studies offer
    url(r"^study-offer/(?P<slug>[\w-]+)/edit/$",
        StudyOfferUpdateView.as_view(),
        name='edit-study-offer'),

    # Upload and list study offer images
    url(r'^study-offer/(?P<slug>[-\w]+)/edit/images/$',
        edit_study_offer_uploads, name='edit_study_offer_uploads'),

    url(r'^study-offer/delete/images/(?P<id>[-\w]+)/$',
        delete_upload_study_offer_image, name='delete_upload_study_offer_image'),


    # Delete of a Study Offer
    url(r"^study-offer/(?P<slug>[\w-]+)/delete/$",
        StudyOfferDeleteView.as_view(),
        name='delete-study-offer'),

    # Search Studies Offer
    url(r'^study-offer/search/$',
        StudiesOffertSearch.as_view(),
        name='studyoffer-search'),

    # Detail of Studies Offert
    # url(r'^study-offer/(?P<pk>\d+)/',
    #    StudyOffertDetailView.as_view(),
    #    name='studyoffertdetail'),

    url(r'^study-offer/(?P<slug>[\w-]+)/$',
        StudyOffertDetailView.as_view(),
        name='studyoffertdetail'),

    url(r'^contact-study-owner/(?P<study_offer_owner_full_name>[\w." "@+-]+)/(?P<study_offer_owner_email>[\w.@+-]+)/from/'
        r'(?P<user_interested_full_name>[\w." "@+-]+)/(?P<user_interested_email>[\w.@+-]+)/'
        r'(?P<study_offer_title>[\w." "@+-]+)/(?P<url_offer>[\w.@+-/]+)/$',
        contact_study_owner_offer,
        name='contact_study_owner_offer'),
]