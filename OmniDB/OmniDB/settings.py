"""
Django settings for OmniDB project.

Generated by 'django-admin startproject' using Django 1.10.6.

For more information on this file, see
https://docs.djangoproject.com/en/1.10/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.10/ref/settings/
"""

import os
import sys
import shutil
import random
import string
import getpass
from . import custom_settings

# Development Mode
DEV_MODE = custom_settings.DEV_MODE

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

TEMP_DIR = os.path.join(BASE_DIR,'OmniDB_app','static','temp')
PLUGINS_DIR = os.path.join(BASE_DIR,'OmniDB_app','static','plugins')

# OmniDB User Folder
DESKTOP_MODE = custom_settings.DESKTOP_MODE
if DEV_MODE:
    HOME_DIR = BASE_DIR
elif custom_settings.HOME_DIR:
    HOME_DIR = custom_settings.HOME_DIR
else:
    if DESKTOP_MODE:
        HOME_DIR = os.path.join(os.path.expanduser('~'), '.omnidb', 'omnidb-app')
    else:
        HOME_DIR = os.path.join(os.path.expanduser('~'), '.omnidb', 'omnidb-server')
if not os.path.exists(HOME_DIR):
    os.makedirs(HOME_DIR)
CHAT_LINK = ''
LOG_DIR = HOME_DIR
SESSION_DATABASE = os.path.join(HOME_DIR, 'db.sqlite3')
if not os.path.exists(SESSION_DATABASE):
    shutil.copyfile(os.path.join(BASE_DIR, 'db.sqlite3'), SESSION_DATABASE)
CONFFILE = os.path.join(HOME_DIR, 'omnidb.conf')
if not DEV_MODE and not os.path.exists(CONFFILE):
    shutil.copyfile(os.path.join(BASE_DIR, 'omnidb.conf'), CONFFILE)
OMNIDB_DATABASE = os.path.join(HOME_DIR, 'omnidb.db')

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.10/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
if DEV_MODE:
    SECRET_KEY = 'ijbq-+%n_(_^ct+qnqp%ir8fzu3n#q^i71j4&y#-6#qe(dx!h3'
else:
    SECRET_KEY = ''.join(random.choice(string.ascii_lowercase + string.digits) for i in range(50))

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = [
    'OmniDB_app.apps.OmnidbAppConfig',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
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

ROOT_URLCONF = 'OmniDB.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'OmniDB.wsgi.application'

# Database
# https://docs.djangoproject.com/en/1.10/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(HOME_DIR, 'db.sqlite3'),
        #'NAME': ':memory:',
    }
}


# Password validation
# https://docs.djangoproject.com/en/1.10/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/1.10/topics/i18n/

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.10/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, "OmniDB_app/static")

SESSION_SERIALIZER = 'django.contrib.sessions.serializers.PickleSerializer'

#OMNIDB LOGGING

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'standard': {
            'format' : "[%(asctime)s] %(levelname)s [%(name)s:%(lineno)s] %(message)s",
            'datefmt' : "%m/%d/%Y %H:%M:%S"
        },
    },
    'handlers': {
        'logfile_omnidb': {
            'class':'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(LOG_DIR, 'omnidb.log'),
            'maxBytes': 1024*1024*5, # 5 MB
            'backupCount': 5,
            'formatter': 'standard',
        },
        'logfile_django': {
            'class':'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(LOG_DIR, 'omnidb.log'),
            'maxBytes': 1024*1024*5, # 5 MB
            'backupCount': 5,
            'formatter': 'standard',
            'level':'ERROR',
        },
        'console_django':{
            'class':'logging.StreamHandler',
            'formatter': 'standard'
        },
        'console_omnidb_app':{
            'class':'logging.StreamHandler',
            'formatter': 'standard',
            'level':'ERROR',
        },
    },
    'loggers': {
        'django': {
            'handlers':['logfile_django','console_django'],
            'propagate': False,
        },
        'OmniDB_app': {
            'handlers': ['logfile_omnidb','console_omnidb_app'],
            'propagate': False,
            'level':'INFO',
        },
        'cherrypy.error': {
            'handlers': ['logfile_django','console_omnidb_app'],
            'level': 'INFO',
            'propagate': False
        }
    }
}

#OMNIDB PARAMETERS
OMNIDB_VERSION                 = custom_settings.OMNIDB_VERSION
OMNIDB_SHORT_VERSION           = custom_settings.OMNIDB_SHORT_VERSION
BINDKEY_AUTOCOMPLETE           = 'ctrl+space'
BINDKEY_AUTOCOMPLETE_MAC       = 'cmd+space'
OMNIDB_WEBSOCKET_PORT          = 25482
OMNIDB_EXTERNAL_WEBSOCKET_PORT = 25482
OMNIDB_ADDRESS                 = '0.0.0.0'
IS_SSL                         = False
SSL_CERTIFICATE                = ""
SSL_KEY                        = ""
CH_CMDS_PER_PAGE               = 20
PWD_TIMEOUT_TOTAL              = 1800
PWD_TIMEOUT_REFRESH            = 300
