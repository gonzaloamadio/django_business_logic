# flake8: noqa

from .base import *

from decouple import config, Csv

DEBUG = True


EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'sqlite3.db' ,
        'USER': '',
        'PASSWORD': '' ,
        'HOST': '',
        'PORT': '',
    }
}

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
    }
}

INSTALLED_APPS += (
    'test_without_migrations',
    'compressor',
    # Django-author ref:https://github.com/lambdalisue/django-author
    # Class decorator to automagically compute "author" and "updated_by" to model
#    'author',
#    'phonenumber_field',
#    'crispy_forms',
    'corsheaders',
#    "fcm_django",
)


CORS_ORIGIN_ALLOW_ALL = True

ALLOWED_HOSTS = []

# So we can put simple pass as 123
PASSWORD_HASHERS = (
    'django.contrib.auth.hashers.MD5PasswordHasher',
)

######### djangotest-no-migrations
TESTING = len(sys.argv) > 1 and sys.argv[1] == 'test'
if TESTING:
    print('=========================')
    print('In TEST Mode - Disableling Migrations')
    print('=========================')

    class DisableMigrations(object):

        def __contains__(self, item):
            return True

        def __getitem__(self, item):
            return
            return "notmigrations"

    MIGRATION_MODULES = DisableMigrations()


########## GRAPH MODEL CONFIG
GRAPH_MODELS = {
  'all_applications': True,
  'group_models': True,
}
########## END GRAPH MODEL CONFIG

########## CORS CONFIG
# https://github.com/ottoyiu/django-cors-headers
# TODO : Configurar algo mas seguro??
CORS_ORIGIN_ALLOW_ALL=True
from corsheaders.defaults import default_headers

