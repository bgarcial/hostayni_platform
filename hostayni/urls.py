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
from django.contrib import admin
from django.conf import settings
from .views import HomePageView

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', HomePageView.as_view(), name='home'),

    # url(r'^$', home, name='home'),

    url(r'^accounts/', include('django.contrib.auth.urls'), name='login'),
    # I don't assign namespace because this is django URL

    # Call the accounts.urls.py
    url(r'^accounts/profiles/', include('accounts.urls', namespace='accounts')),

    # conecta a vistas como logout signup
    # url(r'^accounts/', include('django.contrib.auth.urls')),
    # para autorizacion



]
