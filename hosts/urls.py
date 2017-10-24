from django.conf.urls import url

from .views import (HostingOfferCreateView, HostingOfferUpdateView,
                    StudyOfferCreateView, StudyOffertDetailView,
                    HostingOfferDetailView, lodging_offers_by_user,
                    studies_offers_by_user, StudyOfferUpdateView,
                    LodgingOfferSearch, StudiesOffertSearch,
                    HostingOfferDeleteView, StudyOfferDeleteView,
                    LodgingOfferAjax, contact_owner_offer, contact_study_owner_offer,
                    edit_study_offer_uploads, delete_upload, StudyOfferImageUpdateView
                    )


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

    # Edit Hosting offer
    url(r"^lodging-offer/(?P<slug>[\w-]+)/edit/$",
        HostingOfferUpdateView.as_view(),
        name='edit-lodging-offer'
    ),

    # Delete of a Hosting Offer
    url(r"^lodging-offer/(?P<slug>[\w-]+)/delete/$",
        HostingOfferDeleteView.as_view(),
        name='delete-lodging-offer'
    ),

    # Detail a Hosting Offer

    # url(r"^lodging-offer/(?P<pk>\d+)/$",
    #    HostingOfferDetailView.as_view(),
    #    name='detail'
    # ),

    # Search Hosting Offer
    url(r'^lodging-offer/search/$',
        LodgingOfferSearch.as_view(),
        name='hostingoffer-search'
    ),

    url(r"^lodging-offer/(?P<slug>[\w-]+)/$",
        HostingOfferDetailView.as_view(),
        name='detail'
    ),


    url(r'^contact-to-owner/(?P<lodging_offer_owner_full_name>[\w." "@+-]+)/(?P<lodging_offer_owner_email>[\w.@+-]+)/from/'
        r'(?P<user_interested_full_name>[\w." "@+-]+)/(?P<interested_email>[\w.@+-]+)/'
        r'(?P<lodging_offer_title>[\w." "@+-]+)/(?P<offer_url>[\w.@+-/]+)/$',
        contact_owner_offer,
        name='contact_owner_offer'
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

    # Editando imagen de estudios
    url(r"^study-offer/edit/images/(?P<pk>\d+)/$",
        StudyOfferImageUpdateView.as_view(),
        name='edit-study-offer-image'
    ),

    # Edit Studies offer
    url(r"^study-offer/(?P<slug>[\w-]+)/edit/$",
        StudyOfferUpdateView.as_view(),
        name='edit-study-offer'
    ),

    # Upload study offer images
    url(r'^study-offer/(?P<slug>[-\w]+)/edit/images/$',
        edit_study_offer_uploads, name='edit_study_offer_uploads'
    ),

    #-----
    #url(r'^study-offer/(?P<slug>[-\w]+)/edit/images/(?P<id>[-\w]+)/$',
    #    edit_upload_study_image, name='edit_upload_study_image'),
    # ---



    url(r'^delete/(?P<id>[-\w]+)/$',
        delete_upload, name='delete_upload'),





    # Delete of a Study Offer
    url(r"^study-offer/(?P<slug>[\w-]+)/delete/$",
        StudyOfferDeleteView.as_view(),
        name='delete-study-offer'
    ),

    # Search Studies Offer
    url(r'^study-offer/search/$',
        StudiesOffertSearch.as_view(),
        name='studyoffer-search'
    ),

    # Detail of Studies Offert
    # url(r'^study-offer/(?P<pk>\d+)/',
    #    StudyOffertDetailView.as_view(),
    #    name='studyoffertdetail'
    # ),

    url(r'^study-offer/(?P<slug>[\w-]+)/$',
        StudyOffertDetailView.as_view(),
        name='studyoffertdetail'
    ),

    url(r'^contact-study-owner/(?P<study_offer_owner_full_name>[\w." "@+-]+)/(?P<study_offer_owner_email>[\w.@+-]+)/from/'
        r'(?P<user_interested_full_name>[\w." "@+-]+)/(?P<user_interested_email>[\w.@+-]+)/'
        r'(?P<study_offer_title>[\w." "@+-]+)/(?P<url_offer>[\w.@+-/]+)/$',
        contact_study_owner_offer,
        name='contact_study_owner_offer'
    ),








]