from main.settings.base import *  # noqa


# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False
PRODUCTION = True


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
ADMINS = (
    ('Eshan Das', 'eshan@scientisttechnologies.com'),
)


# Add this if the requests are over SSL
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')


# Celery Flower task url
FLOWER_TASK_URL = '/flower/task/%s'
