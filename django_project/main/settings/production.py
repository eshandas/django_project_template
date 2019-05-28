from .base import *  # noqa
from .base import env


# GENERAL
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#debug
DEBUG = False
# https://docs.djangoproject.com/en/dev/ref/settings/#secret-key
# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'sk&@v$5ab(59+m50nd4mf=gz31$djz6zan0(#brb5v+od2#jm&'



ALLOWED_HOSTS = ['*']


# STATIC FILES
# Django Storages
STATICFILES_STORAGE = 'storages.backends.s3boto.S3BotoStorage'
# Tutorial:
# https://www.caktusgroup.com/blog/2014/11/10/Using-Amazon-S3-to-store-your-Django-sites-static-and-media-files/
# Tell django-storages that when coming up with the URL for an item in S3 storage, keep
# it simple - just use this domain plus the path. (If this isn't set, things get complicated).
# This controls how the `static` template tag from `staticfiles` gets expanded, if you're using it.
# We also use it in the next setting.
AWS_STORAGE_BUCKET_NAME = env('AWS_STORAGE_BUCKET_NAME')
# This will make sure that the file URL does not have unnecessary parameters like your access key.
AWS_QUERYSTRING_AUTH = False
STATIC_URL = 'https://s3-%s.amazonaws.com/%s/' % (AWS_REGION_NAME, AWS_STORAGE_BUCKET_NAME)
AWS_S3_HOST = 's3-%s.amazonaws.com' % AWS_REGION_NAME  # Dont remove this variable, else causes error
MEDIA_URL = STATIC_URL + 'media/'
STATIC_ROOT = 'static'
ADMIN_MEDIA_PREFIX = STATIC_URL + 'admin/'



# List of site admins
ADMINS = ()


# Add this if the requests are over SSL
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')


# Celery Flower task url
FLOWER_TASK_URL = '/flower/task/%s'


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
