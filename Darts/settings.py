"""
Django settings for Darts project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os

import dj_database_url
import django_heroku

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('SECRET_KEY', 'azuqxnu9_3h@mk#f0$afu3=3147cl2v+sy&z=ggjwj^@@k+3q0')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.environ.get('DEBUG') == 'True'

TEMPLATE_DEBUG = DEBUG
CORS_ORIGIN_ALLOW_ALL = True
CORS_ALLOW_METHODS = ('GET',)

# CORS_ORIGIN_WHITELIST = ('leaguecity.uk', 'localhost:8100', 'localhost:8000', 'localhost:8002')
ALLOWED_HOSTS = ['*']
ADMINS = (('Mike', 'mike@saysell.net'))

# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.humanize',
    'django.contrib.staticfiles',
    'django.contrib.sitemaps',
    'markdown_deux',
    'rest_framework',
    'djng',
    'corsheaders',
    'Fixtures',
    'Rules',
    'Darts',
    'derby_darts',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'derby_darts.middleware.leagueware.LeagueMiddleware'
)

ROOT_URLCONF = 'Darts.urls'

WSGI_APPLICATION = 'Darts.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases
DATABASES = {
    'default': dj_database_url.config(default=os.environ.get('DATABASE_URL'))
}

# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/

STATIC_ROOT = '/var/www/html/static/'
STATIC_URL = '/static/'
LOGIN_URL = '/login/'


TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': ["django.contrib.auth.context_processors.auth",
                                   "django.core.context_processors.debug",
                                   "django.core.context_processors.i18n",
                                   "django.core.context_processors.media",
                                   'django.core.context_processors.request']
        }
    },
]

# if not DEBUG:
#     LOGGING = {
#         'version': 1,
#         'disable_existing_loggers': False,
#         'handlers': {
#             'mail_admins': {
#                 'level': 'ERROR',
#                 'class': 'django.utils.log.AdminEmailHandler',
#                 'include_html': True,
#             },
#             'file': {
#                 'level': 'ERROR',
#                 'class': 'logging.FileHandler',
#                 'filename': '/var/log/darts.log'
#             }
#         },
#         'loggers': {
#             'django.request': {
#                 'handlers': ['mail_admins', 'file'],
#                 'level': 'ERROR',
#                 'propagate': True
#             }
#         }
#     }

EMAIL_HOST = 'auth.smtp.1and1.co.uk'
EMAIL_PORT = 587
EMAIL_HOST_USER = 'web@darts.leaguecity.uk'
EMAIL_HOST_PASSWORD = 'oyBbk0wtKv3Hng9MZdan'
EMAIL_USE_TLS = True
DEFAULT_FROM_EMAIL = 'web@darts.leaguecity.uk'

MARKDOWN_DEUX_STYLES = {
    "default": {
        "extras": {
            "code-friendly": None,
        },
        # Allow raw HTML (WARNING: don't use this for user-generated
        # Markdown for your site!).
        "safe_mode": False,
    }
}

django_heroku.settings(locals(), databases=False)