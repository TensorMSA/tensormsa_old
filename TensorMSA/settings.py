"""
Django settings for TensorMSA project.

Generated by 'django-admin startproject' using Django 1.9.5.

For more information on this file, see
https://docs.djangoproject.com/en/1.9/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.9/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.9/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'q4fr0t0g3a=^=#g*b90d2-)$^b+bsl0j$zk-#@f4_#$gkg&7)3'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'tfmsacore.apps.TensormsacoremoduleConfig',
    'tfmsarest.apps.TensormsarestapiConfig',
    'tfmsaview.apps.TfmsaviewConfig',
    'django_jenkins',
    'rest_framework',
    'rest_framework_swagger',
]


MIDDLEWARE_CLASSES = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]


ROOT_URLCONF = 'TensorMSA.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'tfmsaview/templates/')],
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

WSGI_APPLICATION = 'TensorMSA.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.9/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'tensormsa',
        'USER': 'tfmsauser',
        'PASSWORD': '1234',
        'HOST': 'localhost',
        'PORT': '',
    }
}


# Password validation
# https://docs.djangoproject.com/en/1.9/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/1.9/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

TIME = 240 * 60

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.9/howto/static-files/
STATIC_ROOT = os.path.join(BASE_DIR , 'tfmsaview/dist')
STATIC_URL = '/dist/'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "tfmsaview/static/dist"),
]

# custom setting need for tensormsa
SPARK_HOST = '172.32.11.52:7077'
SPARK_CORE = '1'
SPARK_MEMORY = '1G'
SPARK_WORKER_CORE = '2'
SPARK_WORKER_MEMORY = '4G'
HBASE_HOST = '172.32.11.52'
HBASE_HOST_PORT = 9090
PREVIEW_IMG_PATH = os.path.join(BASE_DIR, "tfmsaview/static")
FILE_TEMP_UPLOAD_ROOT = '/tensormsa/temp/file'
FILE_ROOT = '/tensormsa/temp'
HDFS_HOST = '172.32.11.52:9000'
HDFS_ROOT = '/tensormsa'
HDFS_DF_ROOT = '/tensormsa/dataframe'
HDFS_IMG_ROOT = '/tensormsa/image'
HDFS_CONF_ROOT = '/tensormsa/config'
HDFS_TRAIN_ROOT = '/tensormsa/traindata'
HDFS_FORMAT_ROOT = '/tensormsa/format'
HDFS_MODEL_ROOT = '/tensormsa/model'
HDFS_EXTENSION_ROOT = '/tensormsa/extension'
TFMSA_MASTER_SERVER = '172.32.1.21'
TFMSA_TRAIN_SERVER = ['172.31.8.184:8989',]