# -*- coding: utf-8 -*-
from .base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': get_env_variable('DATABASE_NAME'),
        'USER': get_env_variable('DATABASE_USER'),
        'PASSWORD': get_env_variable('DATABASE_PASSWORD'),
        'HOST': 'localhost',
        'PORT': '5432',
    }
}


# STATIC_URL = '/assets/'
# STATICFILES_LOCATION = 'assets'

# MEDIAFILES_LOCATION = 'media/'
# MEDIA_URL = MEDIAFILES_LOCATION

# STATIC_ROOT = os.path.join(BASE_DIR, "assets")
# MEDIA_ROOT = os.path.join(BASE_DIR, "media")