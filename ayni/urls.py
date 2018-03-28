from django.conf.urls import url
from .views import (AyniOfferCreateView, AyniOfferDetailView, AyniOfferUpdateView, AyniOfferDeleteView,
                    AyniOffersByUser, add_ayni_offer_images, delete_ayni_offer_image, AyniOfferImageUpdateView,
                    contact_owner_offer, AyniOfferSearch)

urlpatterns = [

    # Search Ayni Offer
    url(r'^search/$',
        AyniOfferSearch.as_view(),
        name='search'),

    # Create Ayni Offer
    url(r'^new/$',
        AyniOfferCreateView.as_view(),
        name='create'),

    # Detail of a Ayni Offer
    url(r"^(?P<slug>[\w-]+)/$",
        AyniOfferDetailView.as_view(),
        name='detail'),

    # Edit Ayni Offer
    url(r"^(?P<slug>[\w-]+)/edit/$",
        AyniOfferUpdateView.as_view(),
        name='edit'),

    # Delete of a Ayni Offer Offer
    url(r"^(?P<slug>[\w-]+)/delete/$",
        AyniOfferDeleteView.as_view(),
        name='delete'),

    # List Ayni Offer's user
    url(r'^by/u/(?P<username>[-\w]+)/$',
        AyniOffersByUser.as_view(),
        name='list'),

    # Ver todas las imágenes de una oferta de aYNI que han sido subidas y subir una nueva
    # llama a edit_images.html
    url(r'^(?P<slug>[-\w]+)/edit/images/$',
        add_ayni_offer_images, name='edit_images'),

    # Borrar una imagen de una oferta de vida diaria
    url(r'^delete/images/(?P<id>[-\w]+)/$',
        delete_ayni_offer_image, name='delete_img'),

    # Editar una imágen de oferta de emprendimiento de manera individual
    # Llama a entrepreneurshipofferimage_form.html
    url(r"^edit/images/(?P<pk>\d+)/$",
        AyniOfferImageUpdateView.as_view(),
        name='edit_image'),

    url(r'^contact-to-owner/(?P<offer_owner>[\w." "@+-]+)/'
        r'(?P<offer_owner_username>[\w." "@+-]+)/'
        r'(?P<offer_owner_email>[\w.@+-]+)/from/'
        r'(?P<interested_full_name>[\w." "@+-]+)/'
        r'(?P<interested_username>[\w.@+-]+)/'
        r'(?P<interested_email>[\w.@+-]+)/'
        r'(?P<offer_title>[\w." "@+-]+)/(?P<offer_url>[\w.@+-/]+)/$',
        contact_owner_offer, name='contact_owner_offer'),
]