from .settings import *
import os

DEBUG = False
TEMPLATE_DEBUG = False

SECRET_KEY = os.environ.get(
    'SECRET_KEY', 'django-insecure-rt@_xh*11okz20z2wbk&iz6ji*jm-s6+&n*^0(b868hn@q&&2h')

ALLOWED_HOSTS = ['45.55.105.252',]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': '<SET_IT>',
        'USER': '<SET_IT>',
        'PASSWORD': 'password',
        'HOST': '127.0.0.1',
        'PORT': '5432',
    }
}


# Celery settings

REDIS_HOST = os.environ.get('REDIS_HOST', 'localhost')
REDIS_PORT = os.environ.get("REDIS_PORT", 6379)

CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels_redis.core.RedisChannelLayer",
        "CONFIG": {
            "hosts": [(REDIS_HOST, REDIS_PORT)],
        },
        # "ROUTING": "multichat.routing.channel_routing",
    },
}

CELERY_BROKER_URL = os.environ.get("REDIS_TLS_URL", "redis://localhost:6379")
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'

# AWS Console settings
STATICFILES_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID', '')
AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY', '')
AWS_STORAGE_BUCKET_NAME = '<SET_IT>'
AWS_S3_CUSTOM_DOMAIN = '%s.s3.amazonaws.com' % AWS_STORAGE_BUCKET_NAME
AWS_S3_OBJECT_PARAMETERS = {
    'CacheControl': 'max-age=86400',
}
AWS_LOCATION = 'static'

STATIC_URL = 'https://%s/%s/' % (AWS_S3_CUSTOM_DOMAIN, AWS_LOCATION)
STATICFILES_LOCATION = STATIC_URL
DEFAULT_FILE_STORAGE = 'app.storage_backends.BackendS3Storage'

STATIC_URL = "https://%s/%s/" % (AWS_S3_CUSTOM_DOMAIN, STATICFILES_LOCATION)
AWS_PRIVATE_MEDIA_LOCATION = '%'
