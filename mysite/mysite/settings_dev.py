import os

"""
This file contains settings that are specific to the development environment which will override the default
(production) settings declared in settings.py if as environment variable exists called DJANGO_DEVELOPMENT.

I have added this environment variable to my ~/.bashrc file so it will always be present on my laptop.
"""

# local postgres database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'swapdrop_db',
        'USER': 'luka',
        'PASSWORD': 'test123',
        'HOST': 'localhost',
        'PORT': '5432'
    }
}

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')