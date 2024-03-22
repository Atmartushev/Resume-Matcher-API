import os
from dotenv import load_dotenv
"""
Django settings for resumematcherapi project.

Generated by 'django-admin startproject' using Django 5.0.3.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.0/ref/settings/
"""

from pathlib import Path

# Load environment variables from .env file
load_dotenv()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
# Assuming 'settings.py' is inside 'resumematcherapi/resumematcherapi'
# Adjust the path traversal as necessary to point to the project root
BASE_DIR = Path(__file__).resolve().parent.parent

# Use BASE_DIR to construct the path to the .env file
env_file_path = os.path.join(BASE_DIR, '.env')

# Load the .env file
load_dotenv(env_file_path)

# Now attempting to access SECRET_KEY
SECRET_KEY = os.getenv('SECRET_KEY')
if SECRET_KEY is None:
    raise Exception("SECRET_KEY not found. Check your .env file and its path.")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

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
    'core',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'resumematcherapi.urls'

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

WSGI_APPLICATION = 'resumematcherapi.wsgi.application'

# cors port for react
CORS_ALLOWED_ORIGINS = [
    'http://localhost:3000', 
]

# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

import os

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('resume-matcher-aws'),  # Your RDS database name
        'USER': os.getenv('RDS_USERNAME'),  # Your RDS instance username
        'PASSWORD': os.getenv('RDS_PASSWORD'),  # Your RDS password
        'HOST': os.getenv('RDS_HOSTNAME'),  # Your RDS instance endpoint
        'PORT': os.getenv('RDS_PORT', '5432'),  # Your RDS instance port, default is 5432
    }
}



# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

STATIC_URL = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Define the directory where uploaded files will be stored
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')