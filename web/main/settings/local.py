from .base import *  # noqa


# GENERAL
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#debug
DEBUG = True
# https://docs.djangoproject.com/en/dev/ref/settings/#secret-key
# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'k@^dz-i9xdzz+ae=(r97j08cmia(gh73@me!r%-o__qp(1_z8_'


INTERNAL_IPS = ['127.0.0.1']


ALLOWED_HOSTS = ['*']


INSTALLED_APPS += (
    'debug_toolbar',
)


MIDDLEWARE += (
    'debug_toolbar.middleware.DebugToolbarMiddleware',
)


# List of site admins
ADMINS = ()


# Celery Flower task url
FLOWER_TASK_URL = 'http://127.0.0.1:5555/task/%s'
