from django.conf.urls import url


from .views import (DailyLifeOfferCreateView, DailyLifeOfferDetailView, DailyLifeOfferUpdateView,
                    DailyLifeOfferDeleteView, add_daily_life_offer_images, DailyLifeOfferImageUpdateView,
                    delete_daily_life_offer_image, DailyLifeOffersByUser, DailyLifeOfferSearch, contact_owner_offer)


urlpatterns = [

    # Search Daily Life Offer
    url(r'^search/$',
        DailyLifeOfferSearch.as_view(),
        name='search'),


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

    # Delete of a Daily life Offer
    url(r"^(?P<slug>[\w-]+)/delete/$",
        DailyLifeOfferDeleteView.as_view(),
        name='delete'),

    # Ver todas las imágenes de una oferta de vida diaria que han sido subidas y subir una nueva
    # llama a edit_daily_life_offer_images.html
    url(r'^(?P<slug>[-\w]+)/edit/images/$',
        add_daily_life_offer_images, name='edit_images'),

    # Borrar una imagen de una oferta de vida diaria
    url(r'^delete/images/(?P<id>[-\w]+)/$',
        delete_daily_life_offer_image, name='delete_img'),

    # Editar una imágen de oferta de emprendimiento de manera individual
    # Llama a entrepreneurshipofferimage_form.html
    url(r"^edit/images/(?P<pk>\d+)/$",
        DailyLifeOfferImageUpdateView.as_view(),
        name='edit_image'),

    # List Daily life Offer's user
    url(r'^by/u/(?P<username>[-\w]+)/$',
        DailyLifeOffersByUser.as_view(),
        name='list'),

    url(r'^contact-to-owner/(?P<offer_owner>[\w." "@+-]+)/from/'
        r'(?P<offer_owner_email>[\w.@+-]+)/from/to/'
        r'(?P<interested_full_name>[\w." "@+-]+)/'
        r'(?P<interested_email>[\w.@+-]+)/'
        r'(?P<offer_title>[\w." "@+-]+)/(?P<offer_url>[\w.@+-/]+)/$',
        contact_owner_offer, name='contact_owner_offer'),
]