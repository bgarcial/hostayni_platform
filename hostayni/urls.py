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
from .views import HomePageView

from accounts.views import activation_view

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

    # Call the accounts.urls.py
    url(r'^accounts/profiles/', include('accounts.urls', namespace='accounts')),

    url(r'^accounts/', include('django.contrib.auth.urls'), name='login'),
    # I don't assign namespace because this is django URL

    url(r'^accounts/activate/(?P<activation_key>\w+)/$', activation_view, name='activation_view'),



    # conecta a vistas como logout signup
    # url(r'^accounts/', include('django.contrib.auth.urls')),
    # para autorizacion

    url(r'^', include('blog.urls', namespace='articles')),

    url(r'^host/', include('hosts.urls', namespace='host')),

    # Wire up our API using automatic URL routing.
    url(r'^api/', include(router.urls,)),



]

# pARA CARGAR ESTATICOS EN DESARROLLO, No aplica ahora
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

