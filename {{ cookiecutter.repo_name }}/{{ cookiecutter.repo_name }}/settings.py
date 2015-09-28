# -*- coding: utf-8 -*-

"""
Django settings for {{ cookiecutter.project_name }} project.

Generated by 'django-admin startproject' using Django 1.8.3.

For more information on this file, see
https://docs.djangoproject.com/en/1.8/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.8/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os

from decouple import config, Csv

BASE_DIR = os.path.dirname(__file__)


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.8/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config('DEBUG', default=False, cast=bool)

ALLOWED_HOSTS = config('ALLOWED_HOSTS', default='*', cast=Csv())


# Application definition

INSTALLED_APPS = (
    'flat',
    # django
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # 3rd
    {% if cookiecutter.use_compressor == 'y' %}'compressor',{% endif %}
    'crispy_forms',
    'debug_toolbar',
    'django_extensions',
    'django_nose',
    'floppyforms',
    {% if cookiecutter.use_elasticsearch == 'y' %}'haystack',{% endif %}
    'imagekit',
    'rest_framework',
    'rest_framework.authtoken',
    # project
    '{{ cookiecutter.repo_name }}.accounts',
    '{{ cookiecutter.repo_name }}.base',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',
)

ROOT_URLCONF = '{{ cookiecutter.repo_name }}.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, 'templates'),
        ],
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

WSGI_APPLICATION = '{{ cookiecutter.repo_name }}.wsgi.application'

# Database
# https://docs.djangoproject.com/en/1.8/ref/settings/#databases

from dj_database_url import parse as db_url
DATABASES = {'default': config('DATABASE_URL', cast=db_url)}

# Intrnationalization
# https://docs.djangoproject.com/en/1.8/topics/i18n/

LANGUAGE_CODE = 'pt-br'

TIME_ZONE = 'America/Sao_Paulo'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.8/howto/static-files/

STATIC_URL = '/static/'

MEDIA_URL = '/media/'

STATIC_ROOT = os.path.join(BASE_DIR, '..', 'static-root')

MEDIA_ROOT = os.path.join(BASE_DIR, '..', 'media-root')

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
    os.path.join(BASE_DIR, '..', 'bower_components'),
)

{% if cookiecutter.use_compressor == 'y' %}
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'compressor.finders.CompressorFinder',
)

COMPRESS_PRECOMPILERS = (
    # ('text/coffeescript', 'coffee --compile --stdio'),
    # ('text/less', 'lessc --include-path=%s {infile} {outfile}' % STATICFILES_DIRS[1]),  # fuck...
    ('text/x-sass', 'sass --load-path=%s {infile} {outfile}' % STATICFILES_DIRS[1]),
    ('text/x-scss', 'sass --scss --load-path=%s {infile} {outfile}' % STATICFILES_DIRS[1]),
)

COMPRESS_ENABLED = config('COMPRESS_ENABLED', cast=bool, default=False)
COMPRESS_OFFLINE = config('COMPRESS_OFFLINE', cast=bool, default=True)
{% endif %}

# Crispy forms

CRISPY_TEMPLATE_PACK = 'bootstrap3'
CRISPY_FAIL_SILENTLY = not DEBUG

from django.contrib.messages import constants as messages
MESSAGE_TAGS = {
    messages.ERROR: 'danger'
}

# Auth

AUTH_USER_MODEL = 'accounts.User'

LOGIN_URL = '/auth/login/'

LOGOUT_URL = '/auth/logout/'

LOGIN_REDIRECT_URL = '/'

{% if cookiecutter.use_bcrypt == 'y' %}
PASSWORD_HASHERS = (
    'django.contrib.auth.hashers.BCryptSHA256PasswordHasher',
)
{% endif %}

{% if cookiecutter.use_memcached == 'y' %}
# Cache

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
        'LOCATION': config('CACHE_LOCATION'),
    }
}
{% endif %}

{% if cookiecutter.use_elasticsearch == 'y' %}
# Haystack / Elasticsearch

HAYSTACK_CONNECTIONS = {
    'default': {
        'ENGINE': 'haystack.backends.elasticsearch_backend.ElasticsearchSearchEngine',
        'URL': config('HAYSTACK_URL'),
        'INDEX_NAME': 'haystack',
    },
}
{% endif %}

# Tests

TEST_RUNNER = 'django_nose.NoseTestSuiteRunner'

# rest_framework

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.TokenAuthentication',
        'rest_framework.authentication.BasicAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.DjangoModelPermissions',
    ),
    'DEFAULT_FILTER_BACKENDS': (
        'rest_framework.filters.DjangoFilterBackend',
    ),
    'DEFAULT_RENDERER_CLASSES': (
        'rest_framework.renderers.JSONRenderer',
        'rest_framework.renderers.BrowsableAPIRenderer',
        'rest_framework_xml.renderers.XMLRenderer',
    ),
    'DEFAULT_VERSIONING_CLASS': 'rest_framework.versioning.NamespaceVersioning',
    'PAGINATE_BY': 50,
    'MAX_PAGINATE_BY': 300,
    'PAGINATE_BY_PARAM': 'page_size',
}

{% if cookiecutter.use_celery == 'y' %}
# celery

BROKER_URL = config('CELERY_BROKER_URL')

CELERY_IGNORE_RESULT = config('CELERY_IGNORE_RESULT', cast=bool)
CELERY_STORE_ERRORS_EVEN_IF_IGNORED = True

CELERY_TIMEZONE = TIME_ZONE
{% endif %}
