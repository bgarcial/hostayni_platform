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
from django.conf.urls import url, include
from django.conf.urls.static import static
from django.contrib import admin
from django.conf import settings
from .views import WhoWeArePageView, TermsAndConditions, PrivacyPolicy, contact

from accounts.views import activation_view, activate

from hosts.views import LodgingOfferViewSet,StudiesOffertViewSet

from rest_framework import routers

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

    # Call the accounts.urls.py
    url(r'^accounts/profiles/', include('accounts.urls', namespace='accounts')),

    url(r'^accounts/', include('django.contrib.auth.urls'),  name='login'),
    # I don't assign namespace because this is django URL
    # ----------------------------------------------------------------------------------------








    # ----- Nuevo ------#
    # URL para CRUD de posts en la aplicacion web (convencional)
    # y para mapear las busquedas de posts a /post/search/?q=sdsds
    url(r'^post/', include('posts.urls', namespace='post')),
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

    # Wire up our API using automatic URL routing.
    url(r'^api/', include(router.urls,)),


    # -----------Nuevo----------------------#
    # URL para posts de un usuario en REST, salen los posts propios y de los que el sigue
    url(r'^api/', include('accounts.api.urls', namespace='profiles-api')),
    # -----------End Nuevo----------------------#


]

'''
# pARA CARGAR ESTATICOS EN DESARROLLO, No aplica ahora
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
'''

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        url(r'^__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns