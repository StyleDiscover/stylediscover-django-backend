"""
Django settings for clarendon project.

Generated by 'django-admin startproject' using Django 3.1.4.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.1/ref/settings/
"""

from pathlib import Path
import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv("SECRET_KEY")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']

# Application definition

INSTALLED_APPS = [
    # 'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'corsheaders',
    'storages',
    'rest_framework',
    'rest_framework.authtoken',
    'dj_rest_auth',
    'django.contrib.sites',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.facebook',
    'allauth.socialaccount.providers.instagram',
    'dj_rest_auth.registration',
    'knox',
    'users.apps.UsersConfig',
    'components.apps.ComponentsConfig',
    'mainposts.apps.MainpostsConfig',
    'django.contrib.admin',
    'django_extensions'
]

#Variables to be placed in Django project settings.py file
#To define bucket connection details
AWS_STORAGE_BUCKET_NAME = 'stylediscover-media'
AWS_S3_REGION_NAME = 'ap-south-1'  # e.g. us-east-2
AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
#Indicates django-storages the domain to use to refer to static files.
AWS_S3_CUSTOM_DOMAIN = os.getenv("AWS_S3_CUSTOM_DOMAIN")
# AWS_S3_CUSTOM_DOMAIN = '%s.s3.amazonaws.com' % AWS_STORAGE_BUCKET_NAME
AWS_DEFAULT_ACL = None
AWS_S3_OBJECT_PARAMETERS = {
    'CacheControl': 'max-age=86400',
}
#Where to store files (bucket folder name):
STATICFILES_LOCATION = 'static'
#Storage type
STATICFILES_STORAGE = 'custom_storages.StaticStorage'

MEDIAFILES_LOCATION = 'media'
#Storage type
DEFAULT_FILE_STORAGE = 'custom_storages.MediaStorage'

STATIC_URL = '/static/'

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR.joinpath('media')

STATICFILES_DIRS = [BASE_DIR.joinpath('build/static')]

SITE_ID = 2

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'corsheaders.middleware.CorsMiddleware',
]

ROOT_URLCONF = 'clarendon.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR.joinpath('build')],
        'APP_DIRS': True,
        'OPTIONS':
            {
                'context_processors':
                    [
                        'django.template.context_processors.debug',
                        'django.template.context_processors.request',
                        'django.contrib.auth.context_processors.auth',
                        'django.contrib.messages.context_processors.messages',
                    ],
            },
    },
]

WSGI_APPLICATION = 'clarendon.wsgi.application'

# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

if 'DB_HOSTNAME' in os.environ:
    DATABASES = {
        'default':
            {
                'ENGINE': 'django.db.backends.mysql',
                'NAME': os.environ['DB_NAME'],
                'USER': os.environ['DB_USERNAME'],
                'PASSWORD': os.environ['DB_PASSWORD'],
                'HOST': os.environ['DB_HOSTNAME'],
                'PORT': os.environ['DB_PORT'],
            }
    }
else:
    DATABASES = {
        'default':
            {
                'ENGINE': 'django.db.backends.mysql',
                'NAME': os.getenv("DB_NAME"),
                'HOST': os.getenv("DB_HOST"),
                'PORT': os.getenv("DB_PORT"),
                'USER': os.getenv("DB_USER"),
                'PASSWORD': os.getenv("DB_PASSWORD"),
            }
    }

# Email varification
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = os.getenv("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = os.getenv("EMAIL_HOST_PASSWORD")
EMAIL_USE_TLS = True
DEFAULT_FROM_EMAIL = 'Team StyleDiscover <deepak.patidar1235@gmail.com>'

# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME':
            'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME':
            'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME':
            'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME':
            'django.contrib.auth.password_validation.NumericPasswordValidator',
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

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': ('knox.auth.TokenAuthentication', ),
    'DATETIME_FORMAT':
        'iso-8601',
    'DEFAULT_PAGINATION_CLASS':
        'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE':
        3
}

#knox settings
REST_KNOX = {
    'TOKEN_TTL': None,
    'AUTH_HEADER_PREFIX': 'Bearer',
    'AUTH_TOKEN_CHARACTER_LENGTH': 100
}

#knox rest-auth integration
AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
)

REST_AUTH_TOKEN_MODEL = 'knox.models.AuthToken'
REST_AUTH_TOKEN_CREATOR = 'users.utils.create_knox_token'

REST_AUTH_SERIALIZERS = {
    'USER_DETAILS_SERIALIZER': 'users.serializers.UserDetailsSerializer',
    'TOKEN_SERIALIZER': 'users.serializers.KnoxSerializer',
    # 'PASSWORD_RESET_SERIALIZER': 'dj_rest_auth.serializers.PasswordResetSerializer',
    # 'PASSWORD_RESET_CONFIRM_SERIALIZER': 'dj_rest_auth.serializers.PasswordResetConfirmSerializer',
    # 'PASSWORD_CHANGE_SERIALIZER ': 'dj_rest_auth.serializers.PasswordChangeSerializer'
}

SOCIALACCOUNT_PROVIDERS = {
    'facebook': {
        'FIELDS': [
            'id',
            'name',
            'picture',
            'email',
        ]
    },
    'shopify': {
        'IS_EMBEDDED': True
    }
}

REST_AUTH_REGISTER_SERIALIZERS = {
    'REGISTER_SERIALIZER': 'users.serializers.RegisterSerializer'
}
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_EMAIL_VERIFICATION = None

CORS_ORIGIN_ALLOW_ALL = True

AUTH_USER_MODEL = 'users.UserAccount'

ADMINS = []

EMAIL_SUBJECT_PREFIX = '[StyleDiscover]'