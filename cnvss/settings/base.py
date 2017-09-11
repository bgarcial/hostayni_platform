"""
Django settings for cnvss project.

Generated by 'django-admin startproject' using Django 1.11.5.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.11/ref/settings/
"""

import os
from django.core.exceptions import ImproperlyConfigured

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
# which points to the folder containing the actual file, i.e. the folder cnvss.
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))



# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.11/howto/deployment/checklist/

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
    'storages',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'cnvss.urls'

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

WSGI_APPLICATION = 'cnvss.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases

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

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


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

# AUTH_USER_MODEL = "accounts.User"

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