"""
Django settings for cnvss project.

Generated by 'django-admin startproject' using Django 1.10.7.

For more information on this file, see
https://docs.djangoproject.com/en/1.10/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.10/ref/settings/
"""

import os
from django.core.exceptions import ImproperlyConfigured

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
# which points to the folder containing the actual file, i.e. the folder cnvss.
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))



# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.11/howto/deployment/checklist/

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# SECURITY WARNING: keep the secret key used in production secret!
# SECRET_KEY = ''
def get_env_variable(var_name):
    try:
        return os.environ[var_name]
    except KeyError:
        error_msg = "Set the %s environment variable" % var_name
        raise ImproperlyConfigured(error_msg)

SECRET_KEY = get_env_variable('SECRET_KEY')



ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Third party apps
    'debug_toolbar',
    'bootstrap3',
    'django_countries',
    'django_extensions',
    # 'languages_plus',
    'haystack',
    'phonenumber_field',
    'rest_framework',
    # 'smart_selects',
    #'star_ratings',
    'taggit',
    'storages',
    # 'raven.contrib.django.raven_compat',

    # Project apps
    'accounts.apps.AccountsConfig',
    'blog.apps.BlogConfig',
    'host_information.apps.HostInformationConfig',
    'hosts.apps.HostsConfig',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware',
]

ROOT_URLCONF = 'hostayni.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',

        # Like with the static files, Django will look for templates located
        # at a folder named templates inside each app and inside the
        # cnvss/templates folder we just created - root of the site
        'DIRS': [os.path.join(BASE_DIR, "templates")],

        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'hostayni.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.10/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}


# Password validation
# https://docs.djangoproject.com/en/1.11/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/1.11/topics/i18n/

LANGUAGE_CODE = 'es-co'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

REST_FRAMEWORK = {
    # Use Django's standard `django.contrib.auth` permissions,
    # or allow read-only access for unauthenticated users.
    '''
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.TokenAuthentication',
    ),
    '''
    'DEFAULT_PERMISSION_CLASSES': [
        # 'rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly'
        'rest_framework.permissions.AllowAny',
    ],
    'DEFAULT_FILTER_BACKENDS': (
        'django_filters.rest_framework.DjangoFilterBackend',),
}


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.11/howto/static-files/
# This line tells Django to look for static files in a folder named static
# inside each of our apps.
# cnvss_project/cnvss/assets/ - This directory will contain all the static files
# that are global for the project, like CSS or javascript files.

STATIC_URL = '/assets/'


# To tell Django to look for static files in the cnvss/assets directory
# that we just created. With this configuration, Django will look for
# static files in a folder named assets/ inside each app and into the
# cnvss/assets folder we just created.
# BASE_DIR is the root directory
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, "assets"),
)

# https://www.udemy.com/tweetme-django/learn/v4/t/lecture/6134596?start=0 statc serve files
# Usually is a CDN or another server to manage static files
# /webapps/cnvss/assets/
# collectstatic va a static root directory y si no al static
# STATIC_ROOT = os.path.join(BASE_DIR, "assets")


FIXTURE_DIRS = (
   os.path.join(BASE_DIR, 'fixtures'),
)

LOGIN_URL='/accounts/login/'

# Por el momento es asi
LOGIN_REDIRECT_URL = '/'
# La debo enviar al url por ejemplo posts:all

LOGOUT_REDIRECT_URL = LOGIN_REDIRECT_URL

AUTH_USER_MODEL = "accounts.User"

#Amazon S3 Storage
AWS_STORAGE_BUCKET_NAME = get_env_variable('AWS_STORAGE_BUCKET_NAME')
AWS_ACCESS_KEY_ID = get_env_variable('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY =  get_env_variable('AWS_SECRET_ACCESS_KEY')

# Tell django-storages that when coming up with the URL for an item in S3 storage, keep # it simple - just use this domain plus the path.
# (If this isn't set, things get complicated).
# This controls how the `static` template tag from `staticfiles` gets expanded, if you're using it. We also use it in the next setting.
AWS_S3_CUSTOM_DOMAIN = 's3-sa-east-1.amazonaws.com/%s' % AWS_STORAGE_BUCKET_NAME

#MEDIA_URL = "https://%s/" % AWS_S3_CUSTOM_DOMAIN
#MEDIA_ROOT = 'avatars/'
# For media files to S3
STATICFILES_LOCATION = 'assets'
STATICFILES_STORAGE = 'custom_storages.StaticStorage'

STATIC_URL = "https://%s/%s/" % (AWS_S3_CUSTOM_DOMAIN, STATICFILES_LOCATION)

MEDIAFILES_LOCATION = 'media'

MEDIA_URL = "https://%s/%s/" % (AWS_S3_CUSTOM_DOMAIN, MEDIAFILES_LOCATION)

DEFAULT_FILE_STORAGE = 'custom_storages.MediaStorage'



# That will tell boto that when it uploads files to S3, it should set properties on them so that when S3 serves them, it'll include those HTTP headers in the response.
# Those HTTP headers in turn will tell browsers that they can cache these files for a very long time.

AWS_HEADERS = {  # see http://developer.yahoo.com/performance/rules.html#expires
        'Expires': 'Thu, 31 Dec 2199 20:00:00 GMT',
        'Cache-Control': 'max-age=94608000',
    }

BOOTSTRAP3 = {

    # The URL to the jQuery JavaScript file
    'jquery_url': 'https://code.jquery.com/jquery.min.js',

    # The Bootstrap base URL
    'base_url': '//maxcdn.bootstrapcdn.com/bootstrap/3.3.7/',

    # The complete URL to the Bootstrap CSS file (None means derive it from base_url)
    'css_url': None,

    # The complete URL to the Bootstrap CSS file (None means no theme)
    'theme_url': None,

    # The complete URL to the Bootstrap JavaScript file (None means derive it from base_url)
    'javascript_url': None,

    # Put JavaScript in the HEAD section of the HTML document (only relevant if you use bootstrap3.html)
    'javascript_in_head': False,

    # Include jQuery with Bootstrap JavaScript (affects django-bootstrap3 template tags)
    'include_jquery': True,

    # Label class to use in horizontal forms
    'horizontal_label_class': 'col-md-3',

    # Field class to use in horizontal forms
    'horizontal_field_class': 'col-md-9',

    # Set HTML required attribute on required fields, for Django <= 1.8 only
    'set_required': True,

    # Set HTML disabled attribute on disabled fields, for Django <= 1.8 only
    'set_disabled': False,

    # Set placeholder attributes to label if no placeholder is provided
    'set_placeholder': True,

    # Class to indicate required (better to set this in your Django form)
    'required_css_class': '',

    # Class to indicate error (better to set this in your Django form)
    'error_css_class': 'has-error',

    # Class to indicate success, meaning the field has valid input (better to set this in your Django form)
    'success_css_class': 'has-success',

    # Renderers (only set these if you have studied the source and understand the inner workings)
    'formset_renderers':{
        'default': 'bootstrap3.renderers.FormsetRenderer',
    },
    'form_renderers': {
        'default': 'bootstrap3.renderers.FormRenderer',
    },
    'field_renderers': {
        'default': 'bootstrap3.renderers.FieldRenderer',
        'inline': 'bootstrap3.renderers.InlineFieldRenderer',
    },
}


HAYSTACK_CONNECTIONS = {
    'default': {
        'ENGINE': 'haystack.backends.solr_backend.SolrEngine',
        'URL': 'http://127.0.0.1:8983/solr/hostayni'
    },
}

HAYSTACK_SIGNAL_PROCESSOR = 'haystack.signals.RealtimeSignalProcessor'


EMAIL_HOST = get_env_variable('EMAIL_HOST')
EMAIL_HOST_USER = get_env_variable('EMAIL_HOST_USER')

# Sender
DEFAULT_FROM_EMAIL = ' HOSTAYNI <hello@hostayni.com>'
EMAIL_HOST_PASSWORD = get_env_variable('EMAIL_HOST_PASSWORD')
EMAIL_PORT = 587
EMAIL_USE_TLS = True

SITE_URL = 'http://www.hostayni.com'

'''
if DEBUG:
    SITE_URL = 'http://127.0.0.1:8000'
    #SITE_URL = 'http://www.hostayni.com'
'''


"""
from django.conf import settings
from django.core.mail import send_mail

send_mail('Notificación de hostayni correo', 'El correo noreply@hostayni.com es ficticio, debemos decidir
   ...:  que correo estará como remitente de las notificaciones a correo electrónico y comprarlo ya para tener im
   ...: plementada esta funcionalidad de notificar a correo electrónico. Estamos usando el servicio de sendgrid.c
   ...: om', 'noreply@hostayni.com', ['botibagl@gmail.com', 'bmlugar@gmail.com','christiandiazleon@gmail.com','ju
   ...: anjaimearroyaver@gmail.com'], fail_silently=False)

    
send_mail(
    "subject", 
    "here is the message", 
    from_email, 
    to_email_list, # must be a list
    fail_silently=False)
"""