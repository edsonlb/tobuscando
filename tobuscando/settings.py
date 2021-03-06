# coding: utf-8
import os
from django.conf.global_settings import TEMPLATE_CONTEXT_PROCESSORS as TCP
from decouple import config
from dj_database_url import parse as db_url

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config('SECRET_KEY')

DEBUG = config('DEBUG', default=True)

TEMPLATE_DEBUG = True

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

# SECRET TOKEN: for email validation
SECRET_TOKEN = config('SECRET_TOKEN', cast=int)

ALLOWED_HOSTS = [
    '.locahost:*', '127.0.0.1:*', 'tobuscando.herokuapp.com',
    'tobuscando.com', 'www.tobuscando.com', 'tobuscando.com.br'
]

SITE_URL = 'http://www.tobuscando.com'

# 1 = OFFLINE / 2 = ONLINE
SITE_ID = 2

AUTH_USER_MODEL = 'core.Person'

# Application definition
TEMPLATE_CONTEXT_PROCESSORS = TCP + (
    'django.core.context_processors.request',
    "django.contrib.auth.context_processors.auth",
    "django.core.context_processors.debug",
    "django.core.context_processors.i18n",
    "django.core.context_processors.media",
    "django.core.context_processors.static",
    "django.core.context_processors.tz",
    "django.contrib.messages.context_processors.messages",
    "django.core.context_processors.request",
    "allauth.account.context_processors.account",
    "allauth.socialaccount.context_processors.socialaccount",
)

INSTALLED_APPS = (
    'suit',
    'django.contrib.admin',
    'django.contrib.sites',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.auth',
    'django.contrib.flatpages',

    'tobuscando.core',
    'tobuscando.dashboard',
    'tobuscando.ads',
)

"""
It's a External Apps.

** Please, don't remove it, you can do stop run allauth if to change it. **

For default, the allauth apps are for last. EVER!

"""

INSTALLED_APPS += (
    'south',
    'cloudinary',
    'smart_selects',
    'mptt',
    'bootstrap3',

    'pagination',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.facebook',
    'allauth.socialaccount.providers.twitter',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'pagination.middleware.PaginationMiddleware',
)


AUTHENTICATION_BACKENDS = (
    "django.contrib.auth.backends.ModelBackend",
    "allauth.account.auth_backends.AuthenticationBackend",
)

ROOT_URLCONF = 'tobuscando.urls'

WSGI_APPLICATION = 'tobuscando.wsgi.application'

AUTH_PROFILE_MODULE = "sistema_sga.profile.profile"

# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

DATABASES = {
    'default': config(
        'DATABASE_URL',
        default='sqlite:///{0}'.format(os.path.join(BASE_DIR, 'db.sqlite3')),
        cast=db_url)
}


LOGIN_URL = '/accounts/login/'
LOGIN_REDIRECT_URL = '/dashboard/'

ACCOUNT_ADAPTER = "allauth.account.adapter.DefaultAccountAdapter"
ACCOUNT_AUTHENTICATION_METHOD = "username_email"
ACCOUNT_CONFIRM_EMAIL_ON_GET = "optional"
ACCOUNT_EMAIL_CONFIRMATION_ANONYMOUS_REDIRECT_URL = LOGIN_URL
ACCOUNT_EMAIL_CONFIRMATION_AUTHENTICATED_REDIRECT_URL = LOGIN_REDIRECT_URL
ACCOUNT_EMAIL_CONFIRMATION_EXPIRE_DAYS = 10
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_EMAIL_VERIFICATION = True
ACCOUNT_EMAIL_SUBJECT_PREFIX = "Assunto: "
ACCOUNT_DEFAULT_HTTP_PROTOCOL = "http"
ACCOUNT_LOGOUT_ON_GET = True
ACCOUNT_LOGOUT_REDIRECT_URL = LOGIN_URL
ACCOUNT_SIGNUP_FORM_CLASS = None    # 'tobuscando.core.forms.SignupForm'
ACCOUNT_SIGNUP_PASSWORD_VERIFICATION = True
ACCOUNT_UNIQUE_EMAIL = True
ACCOUNT_USER_MODEL_USERNAME_FIELD = "username"
ACCOUNT_USER_MODEL_EMAIL_FIELD = "email"
# ACCOUNT_USER_DISPLAY (=a callable returning user.username)
ACCOUNT_USERNAME_MIN_LENGTH = 4
ACCOUNT_USERNAME_BLACKLIST = ['some_username_youdon\t_want']
ACCOUNT_USERNAME_REQUIRED = True
ACCOUNT_PASSWORD_INPUT_RENDER_VALUE = False
ACCOUNT_PASSWORD_MIN_LENGTH = 6
ACCOUNT_LOGIN_ON_EMAIL_CONFIRMATION = True

SOCIALACCOUNT_PROVIDERS = {
    'facebook': {
        'SCOPE': ['email', 'publish_stream'],
        'AUTH_PARAMS': {'auth_type': 'https'},
        'METHOD': 'oauth2',
        'VERIFIED_EMAIL': False
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'pt-BR'

# MANUAL PARA GERAÃ‡ÃƒO DAS TRADUÃ‡Ã•ES
# django-admin.py makemessages -l pt-br
# django-admin.py compilemessages -l pt-br

LANGUAGE = (
    ('pt-br', u'PortuguÃªs'),
    ('en-us', u'English'),
    ('es', u'EspaÃ±ol'),
)

LOCALE_PATHS = (
    os.path.join(BASE_DIR, 'locale'),
)

TIME_ZONE = 'America/Sao_Paulo'

USE_I18N = True

USE_L10N = True

USE_TZ = True

MPTT_LEVEL_INDENT = 20

STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

STATIC_URL = '/static/'

CLOUDINARY = {
    'cloud_name': 'to-buscando',  # config('CLOUDINARY_NAME'),
    'api_key': '',   # config('CLOUDINARY_API_KEY'),
    # config('CLOUDINARY_API_SECRET')
    'api_secret': ''
}

MAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

"""
EMAIL_HOST = config('EMAIL_HOST')
EMAIL_HOST_USER = config('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD')
EMAIL_PORT = 587    # config('EMAIL_PORT', cast=int)
EMAIL_USE_TLS = config('EMAIL_USE_TLS', default=False)
"""


#NÃ£o usar Gmail, fazer o possÃ­vel para usar o oficial.
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'nao_responda@.com.br'
EMAIL_HOST_PASSWORD = ''
EMAIL_PORT = 587
EMAIL_USE_TLS = True
