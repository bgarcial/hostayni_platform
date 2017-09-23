from __future__ import unicode_literals
from django.conf.urls import url, include
from django.conf import settings
from . import views

urlpatterns = [
    # auth_views.LoginView es la vista de login en Django 1.11 para cuando actualicemos
    # url(r"login/$", auth_views.LoginView.as_view(template_name='accounts/login.html'), name='login'),

    # auth_views.LogoutView es la vista de logout en Django 1.11 para cuando actualicemos
    # url(r"logout/$", auth_views.LogoutView.as_view(), name="logout"),

    url(r"logout/$", views.LogoutView.as_view(), name="logout"),
    url(r"signup/$", views.SignUpView.as_view(), name="signup"),

    url(r"^preferences/u/(?P<slug>[\w.\-]+)/$", views.AccountSettingsUpdateView.as_view(), name='preferences'),

    url(r"^data/u/(?P<slug>[\w\-]+)/$", views.user_profile_update_view, name='profile'),
]