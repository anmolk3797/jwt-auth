"""
Django settings for jwt_auth project.

Generated by 'django-admin startproject' using Django 3.1.4.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.1/ref/settings/
"""

import os
import sys
# from pathlib import Path
from unipath import Path
from datetime import timedelta

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Build paths inside the project like this: os.path.join(BASE_DIR, ...)

PROJECT_DIR = Path(__file__).ancestor(2)
PROJECT_APPS = Path(__file__).ancestor(2)

sys.path.insert(0, Path(PROJECT_APPS, 'apps'))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.environ.get('DEBUG')

# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

DATABASES = {
    'default': {
        'NAME':     os.environ.get("DATABASE_NAME"),
        'USER':     os.environ.get("DATABASE_USERNAME"),
        'PASSWORD': os.environ.get("DATABASE_PASSWORD"),
        'HOST':     os.environ.get("DATABASE_HOST"),
        'PORT':     os.environ.get("DATABASE_PORT"),
        "tz_aware": True,
    }
}

ALLOWED_HOSTS = []

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'rest_framework_swagger',
    'rest_framework.authtoken',
    'corsheaders',
    'drf_yasg',         # doc
    'django_crontab',   # cron
    "oauth2_provider",  # OAuth2
    "schema_graph",
    "django_extensions",

    # apps
    'apps.authentication',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]


REST_AUTH_SERIALIZERS = {
    'PASSWORD_RESET_SERIALIZER':
        'authentication.serializers.PasswordResetSerializer',
}

ROOT_URLCONF = 'jwt_auth.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
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

WSGI_APPLICATION = 'jwt_auth.wsgi.application'

# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/

# media files (Pdf, Images)
# MEDIA_ROOT = PROJECT_DIR.child('media')
MEDIA_ROOT = os.path.join(BASE_DIR, "media")

MEDIA_URL = '/media/'

# Static files (CSS, JavaScript, Images, Pdf)
STATIC_ROOT = PROJECT_DIR.child('staticfiles')

STATIC_URL = '/static/'

# STATICFILES_DIRS = [
#     PROJECT_DIR.child("static"),
# ]

# BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# STATIC_ROOT = os.path.normpath(os.path.join(BASE_DIR, 'staticfiles'))
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
)

CLIENT_ID = os.environ.get("CLIENT_ID")
CLIENT_SECRET = os.environ.get("CLIENT_SECRET")

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    # 'oautsh2_provider.backends.OAuth2Backend',

)



AUTH_USER_MODEL = 'authentication.User'
# AUTH_USERNAME_FIELD = 'email'

MONGOENGINE_USER_DOCUMENT = 'authentication.models.User'

LOGIN_REDIRECT = 'authentication:login'
SIGNUP_REDIRECT = 'authentication:signup'

SITE_ID = 1

CORS_ORIGIN_ALLOW_ALL = True

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
EMAIL_USE_TLS = True
EMAIL_HOST = "smtp.gmail.com"
EMAIL_HOST_USER = os.environ.get("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = os.environ.get("EMAIL_HOST_PASSWORD")
EMAIL_PORT = 587

REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 10,
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
}

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(days=365),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=365),
    'ROTATE_REFRESH_TOKENS': False,
    'BLACKLIST_AFTER_ROTATION': True,

    'ALGORITHM': 'HS256',
    #'SIGNING_KEY': settings.SECRET_KEY,
    'VERIFYING_KEY': None,

    'AUTH_HEADER_TYPES': ('Bearer',),
    'USER_ID_FIELD': 'id',
    'USER_ID_CLAIM': 'user_id',

    'AUTH_TOKEN_CLASSES': ('rest_framework_simplejwt.tokens.AccessToken',),
    'TOKEN_TYPE_CLAIM': 'token_type',

    'JTI_CLAIM': 'jti',

    'SLIDING_TOKEN_REFRESH_EXP_CLAIM': 'refresh_exp',
    'SLIDING_TOKEN_LIFETIME': timedelta(minutes=5),
    'SLIDING_TOKEN_REFRESH_LIFETIME': timedelta(days=1),
}