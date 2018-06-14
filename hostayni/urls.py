"""hostayni URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static

from django.conf.urls import url, include

from django.contrib import admin

from .views import WhoWeArePageView, TermsAndConditions, PrivacyPolicy, contact, \
    HowItWorksPageView, HowTheOffersWorksPageView

from accounts.views import activation_view, activate

from hosts.views import LodgingOfferViewSet, StudiesOffertViewSet

from rest_framework import routers
from posts.api.views import SearchPostAPIView
from hashtags.views import HashTagView
from hashtags.api.views import TagPostAPIView


# Routers provide an easy way of automatically determining the URL conf.
router = routers.DefaultRouter()
router.register(r'lodging-offers', LodgingOfferViewSet)
router.register(r'studies-offers', StudiesOffertViewSet)

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    # url(r'^$', HomePageView.as_view(), name='home'),

    # url(r'^$', home, name='home'),
    url(r'^who-we-are/$', WhoWeArePageView.as_view(), name='who-we-are'),

    url(r'^terms-and-conditions/$', TermsAndConditions.as_view(), name='terms-and-conditions'),

    url(r'^privacy-policy/$', PrivacyPolicy.as_view(), name='privacy-policy'),
    url(r'^contact/$', contact, name='contact'),

    url(r'^how-it-works/$', HowItWorksPageView.as_view(), name='how-it-works'),

    url(r'^how-the-offers-works/$', HowTheOffersWorksPageView.as_view(), name='how-the-offers-works'),

    # Call the accounts.urls.py
    url(r'^accounts/profiles/', include('accounts.urls', namespace='accounts')),

    url(r'^accounts/', include('django.contrib.auth.urls'),  name='login'),
    # I don't assign namespace because this is django URL
    # ----------------------------------------------------------------------------------------

    #url(r"^(?P<username>[\w\-]+)/$", UserDetailView.as_view(), name='detail'),

    url(r'^carousel-marketing/', include('carousel_offers.urls', namespace='carousels')),


    # ----- Nuevo ------#
    url(r'^tags/(?P<hashtag>.*)/$', HashTagView.as_view(), name='hashtag'),
    # ----- End Nuevo ------#


    # ----- Nuevo ------#
    # URL para CRUD de posts en la aplicacion web (convencional)
    # y para mapear las busquedas de posts a /post/search/?q=sdsds
    url(r'^post/', include('posts.urls', namespace='post')),
    # ----- End Nuevo ------#\

    # ----- Nuevo ------#\
    url(r'^api/tags/(?P<hashtag>.*)/$', TagPostAPIView.as_view(), name='tag-post-api'), #
    # ----- End Nuevo ------#\

    # ----- Nuevo ------#
    # Buscando en Hostayni social seria /api/search/
    url(r'^api/search/$', SearchPostAPIView.as_view(), name='search-api'), #
    # ----- End Nuevo ------#


    # ----- Nuevo ------#
    # URL para los posts en el sistema de quienes sigo
    url(r'^api/post/', include('posts.api.urls', namespace='post-api')),
    # ----- End Nuevo ------#










    # ----------------------------------------------------------------------------------------------
    # url(r'^accounts/activate/(?P<activation_key>\w+)/$', activation_view, name='activation_view'),
    url(r'^accounts/activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$', activate, name='activate'),


    # conecta a vistas como logout signup
    # url(r'^accounts/', include('django.contrib.auth.urls')),
    # para autorizacion

    url(r'^', include('blog.urls', namespace='articles')),

    url(r'^host/', include('hosts.urls', namespace='host')),

    url(r'^daily-life-offer/', include('daily_life.urls', namespace='daily_life_offer')),

    url(r'^offer/entrepreneurship/', include('entrepreneurship.urls', namespace='offer')),

    url(r'^ayni-offer/', include('ayni.urls', namespace='ayni_offer')),


    # Wire up our API using automatic URL routing.
    url(r'^api/', include(router.urls,)),


    # url(r'^api-auth/', include('rest_framework.urls',
    #    namespace='rest_framework')),

    # -----------Nuevo----------------------#
    # URL para posts de un usuario en REST, salen los posts propios y de los que el sigue
    url(r'^api/', include('accounts.api.urls', namespace='profiles-api')),
    # -----------End Nuevo----------------------#


]


# pARA CARGAR ESTATICOS EN DESARROLLO,
if settings.DEBUG:
    urlpatterns = urlpatterns + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns = urlpatterns + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

'''
if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        url(r'^__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns
'''
