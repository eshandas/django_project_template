from main.settings.base import *


# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True


INTERNAL_IPS = ['127.0.0.1']


ALLOWED_HOSTS = ['*']


INSTALLED_APPS += (
    'debug_toolbar',
)


MIDDLEWARE += (
    'debug_toolbar.middleware.DebugToolbarMiddleware',
)


# List of site admins
ADMINS = (
    ('Eshan Das', 'eshan@scientisttechnologies.com'),
)


# Celery Flower task url
FLOWER_TASK_URL = 'http://127.0.0.1:5555/task/%s'
