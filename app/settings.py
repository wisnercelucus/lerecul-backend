from datetime import timedelta
from pathlib import Path
import os
# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'django-insecure-rt@_xh*11okz20z2wbk&iz6ji*jm-s6+&n*^0(b868hn@q&&2h'

dev_env = os.environ.get('DEV_ENV', None)

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']


# Application definition
FRONT_URL = os.environ.get("FRONT_URL", 'localhost:4200')

if not dev_env:
    DEBUG = False
    FRONT_URL = os.environ.get("FRONT_URL", '<your domain>')
    # MY_PROD_DOMAIN = 'smartlysms.com'
    # MY_PROD_API_DOMAIN = '.smartly-sms.com'
    # MY_ROOT_API_DOMAIN = 'smartly-sms.com'
    # FRONT_URL = 'smartlysms.com'


INSTALLED_APPS = [
    "daphne",
    'channels',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    "corsheaders",
    'django_rest_passwordreset',
    'storages',
    'accounts',
    'core',
    'model_meta_data',
    'modelrelations',
    'core_forms',
    'frontend_views',
    'loginactivity',
    'home',
    'documents',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    "corsheaders.middleware.CorsMiddleware",
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'app.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

ASGI_APPLICATION = 'app.routing.application'
WSGI_APPLICATION = 'app.wsgi.application'

AUTH_USER_MODEL = 'accounts.User'


# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

# DATABASES = {
#    'default': {
#        'ENGINE': 'django.db.backends.sqlite3',
#        'NAME': BASE_DIR / 'db.sqlite3',
#    }
# }

if DEBUG:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': '<DB_NAME>',
            'USER': '<DB_USER>',
            'PASSWORD': '<DB_PASSWORD>',
            'HOST': 'localhost',
            'PORT': '5432',
        }
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': '<PROD_DB_NAME>',
            'USER': '<PROD_DB_USER>',
            'PASSWORD': '<PROD_DB_PASSWORD>',
            'HOST': 'localhost',
            'PORT': '5432',
        }
    }

# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/4.1/topics/i18n/

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/


STATICFILES_DIRS = [
    # dev only after collecting static schemas
    os.path.join(BASE_DIR, "static"),
]

# STATIC_URL = 'static/'

STATIC_URL = '/static/'
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles/')

# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


CORS_ALLOWED_ORIGINS = [
    "http://localhost:4200",
]

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.AllowAny',
    ]
}

PASSWORD_LENGTH = 10
CODE_LENGTH = 6


SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=2880),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),
    'ROTATE_REFRESH_TOKENS': False,
    'BLACKLIST_AFTER_ROTATION': False,
    'UPDATE_LAST_LOGIN': False,

    'ALGORITHM': 'HS256',
    'SIGNING_KEY': SECRET_KEY,
    'VERIFYING_KEY': None,
    'AUDIENCE': None,
    'ISSUER': None,
    'JWK_URL': None,
    'LEEWAY': 0,

    'AUTH_HEADER_TYPES': ('Bearer',),
    'AUTH_HEADER_NAME': 'HTTP_AUTHORIZATION',
    'USER_ID_FIELD': 'id',
    'USER_ID_CLAIM': 'user_id',
    'USER_AUTHENTICATION_RULE': 'rest_framework_simplejwt.authentication.default_user_authentication_rule',

    'AUTH_TOKEN_CLASSES': ('rest_framework_simplejwt.tokens.AccessToken',),
    'TOKEN_TYPE_CLAIM': 'token_type',
    'TOKEN_USER_CLASS': 'rest_framework_simplejwt.models.TokenUser',

    'JTI_CLAIM': 'jti',

    'SLIDING_TOKEN_REFRESH_EXP_CLAIM': 'refresh_exp',
    'SLIDING_TOKEN_LIFETIME': timedelta(minutes=2880),
    'SLIDING_TOKEN_REFRESH_LIFETIME': timedelta(days=7),
}

DJANGO_REST_MULTITOKENAUTH_RESET_TOKEN_EXPIRY_TIME = 24


EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.mailgun.org'

LOCAL_MAILGUN_EMAIL_HOST_PASSWORD = os.environ.get(
    "LOCAL_MAILGUN_EMAIL_HOST_PASSWORD", '')
# print(LOCAL_MAILGUN_EMAIL_HOST_PASSWORD)
EMAIL_HOST_USER = os.environ.get('MAILGUN_EMAIL_HOST_USER', '')
EMAIL_HOST_PASSWORD = os.environ.get(
    'MAILGUN_EMAIL_HOST_PASSWORD', LOCAL_MAILGUN_EMAIL_HOST_PASSWORD)
EMAIL_USE_TLS = True
EMAIL_PORT = 587
DEFAULT_FROM_EMAIL = os.environ.get('MAILGUN_EMAIL_SENDER', '')
SYSTEM_EMAIL_RECEIVER = '<SET_IT>'
EMAIL_ADMIN_TO = SYSTEM_EMAIL_RECEIVER
REDIS_URL = os.environ.get("REDIS_TLS_URL", "redis://localhost:6379")

CELERY_BROKER_URL = REDIS_URL
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'


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


# Internationalization

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True
TEMPUS_DOMINUS_LOCALIZE = True

SITE_ROOT = os.path.dirname(os.path.realpath(__name__))
LOCALE_PATHS = (os.path.join(SITE_ROOT, 'locale'), )

LANGUAGES = [
    ('en', 'English'),
    ('en-US', 'English'),
    ('es', 'Spanish'),
    ('es-ES', 'Spanish'),
    ('fr', 'French'),
    ('fr-FR', 'French'),
]

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
