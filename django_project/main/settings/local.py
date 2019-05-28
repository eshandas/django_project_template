from .base import *  # noqa
from .base import env


# GENERAL
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#debug
DEBUG = True
# https://docs.djangoproject.com/en/dev/ref/settings/#secret-key
# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'or8)j(+#sf7j)-od-u9hf^3fph693_3x1=ja2q9mpu3+pv@b-b'


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
ADMINS = ()


# Celery Flower task url
FLOWER_TASK_URL = 'http://127.0.0.1:5555/task/%s'


# Email server settings
# ABSOLUTELY REMOVE THE DUMMY EMAIL SERVER IN PRODUCTION!!!
# EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
EMAIL_BACKEND = 'django_smtp_ssl.SSLEmailBackend'
EMAIL_USE_TLS = True
EMAIL_HOST = env('EMAIL_HOST')
EMAIL_PORT = env('EMAIL_PORT')
EMAIL_HOST_USER = env('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = env('EMAIL_HOST_PASSWORD')
EMAIL_FROM = env('EMAIL_FROM')
