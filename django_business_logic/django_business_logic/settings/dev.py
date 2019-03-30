# flake8: noqa

from .base import *

from decouple import config, Csv

DEBUG = config('DEBUG', default=True, cast=bool)


EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': config('DB_NAME'),
        'USER': config('DB_USER'),
        'PASSWORD': config('DB_PASSWORD'),
        'HOST': config('DB_HOST'),
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

ALLOWED_HOSTS = config('ALLOWED_HOSTS', cast=Csv())

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



########## DJANGO-DEBUG-TOOLBAR CONFIGURATION
#MIDDLEWARE_CLASSES += (
#    'debug_toolbar.middleware.DebugToolbarMiddleware',
#)
#INSTALLED_APPS += (
#    'debug_toolbar',
#)

# IPs allowed to see django-debug-toolbar output.
INTERNAL_IPS = ('10.11.11.xx','127.0.0.1','localhost')

DEBUG_TOOLBAR_CONFIG = {
    # If set to True (default), the debug toolbar will show an intermediate
    # page upon redirect so you can view any debug information prior to
    # redirecting. This page will provide a link to the redirect destination
    # you can follow when ready. If set to False, redirects will proceed as
    # normal.
    'INTERCEPT_REDIRECTS': False,

    'SHOW_TOOLBAR_CALLBACK': lambda *args: True,

    # An array of custom signals that might be in your project, defined as the
    # python path to the signal.
    'EXTRA_SIGNALS': [],

    # If set to True (the default) then code in Django itself won't be shown in
    # SQL stacktraces.
    'HIDE_DJANGO_SQL': True,

    # If set to True (the default) then a template's context will be included
    # with it in the Template debug panel. Turning this off is useful when you
    # have large template contexts, or you have template contexts with lazy
    # datastructures that you don't want to be evaluated.
    'SHOW_TEMPLATE_CONTEXT': True,

     # If set, this will be the tag to which debug_toolbar will attach the debug
     # toolbar. Defaults to 'body'.
     'TAG': 'body',
}
#def show_toolbar(request):
#    return True
#if settings.DEBUG:
#    import debug_toolbar
########## END DJANGO-DEBUG-TOOLBAR CONFIGURATION

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

CORS_ALLOW_HEADERS = default_headers + (
    'Token',
)
########## CORS CONFIG END

######### DOCUMENTACION SPHINX
# Docuemntacion sphinx
# Sphinx 0.9.9
SPHINX_API_VERSION = 0x116


