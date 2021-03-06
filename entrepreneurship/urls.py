from django.conf.urls import url
from .views import (EntrepreneurshipOfferCreateView, EntrepreneurshipOfferDetailView,
                    EntrepreneurshipOfferUpdateView, EntrepreneurshipOfferDeleteView,
                    entrepreneurship_offers_by_user, EntrepreneurshipOffersByUser,
                    add_entrepreneurship_offer_images, EntrepreneurshipOfferImageUpdateView,
                    contact_owner_offer, EntrepreneurshipOfferSearch, delete_entrepreneurship_offer_image)

urlpatterns = [

    # Create Entrepreneurship Offer
    url(r'^new/$',
        EntrepreneurshipOfferCreateView.as_view(),
        name='create'),

    # Search Entrepreneurship Offer
    url(r'^search/$',
        EntrepreneurshipOfferSearch.as_view(),
        name='entrepreneurship_offer_search'),


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

    # Ver todas las imágenes de oferta de emprendimiento que han sido subidas y subir una nueva
    # llama a edit_entrepreneurship_offer_images.html
    url(r'^(?P<slug>[-\w]+)/edit/images/$',
        add_entrepreneurship_offer_images, name='edit_entrepreneurship_images'),

    # Borrar una imagen de una oferta de emprendimiento
    url(r'^lodging-offer/delete/images/(?P<id>[-\w]+)/$',
        delete_entrepreneurship_offer_image, name='delete_offer_image'),


    # Editar una imágen de oferta de emprendimiento de manera individual
    # Llama a entrepreneurshipofferimage_form.html
    url(r"^edit/images/(?P<pk>\d+)/$",
        EntrepreneurshipOfferImageUpdateView.as_view(),
        name='edit_entrepreneurship_offer_image'),


    url(r'^contact-to-owner/(?P<offer_owner>[\w." "@+-]+)/from/'
        r'(?P<offer_owner_email>[\w.@+-]+)/to/'
        r'(?P<interested_full_name>[\w." "@+-]+)/'
        r'(?P<interested_email>[\w.@+-]+)/'
        r'(?P<offer_title>[\w." "@+-]+)/(?P<offer_url>[\w.@+-/]+)/$',
        contact_owner_offer, name='contact_owner_offer'),



    ]

