"""
Django settings for hello project.

Generated by 'django-admin startproject' using Django 5.0.4.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.0/ref/settings/
"""

from pathlib import Path
# added by me
from decouple import config

# form templates
from django.forms.renderers import TemplatesSetting

# follow the CORS example
import mimetypes
mimetypes.add_type("text/css", ".css", True)


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
#SECRET_KEY = 'django-insecure-5%\-r#@4-(j=g8m*m^7e6wi*vs7vb+7^@al82tezhpzme1##f80'
SECRET_KEY = config("SECRET_KEY", "")

# SECURITY WARNING: don't run with debug turned on in production!
#DEBUG = True
DEBUG = config("DEBUG", default=True)

#ALLOWED_HOSTS = []
ALLOWED_HOSTS = config("ALLOWED_HOSTS", default="").split(",")

# Following the cors example
CSRF_TRUSTED_ORIGINS = ['https://*.azurewebsites.net','http://localhost:8000']
CORS_ALLOW_ALL_ORIGINS: True


# Application definition

INSTALLED_APPS = [
    # added by me, follow the configuration guide in microsoft
    'whitenoise.runserver_nostatic',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_browser_reload',
    # following cors example
    'rest_framework',
    'corsheaders',
    'home',
    'bands',
    'content',
]

# Following the cors example
CORS_ORIGIN_ALLOW_ALL = True


MIDDLEWARE = [
    # following the cors example
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django_browser_reload.middleware.BrowserReloadMiddleware',
]

# need to confirm this root
ROOT_URLCONF = 'hello.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'hello' / 'templates',
                 BASE_DIR / 'templates',
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

WSGI_APPLICATION = 'hello.wsgi.application'

# SQLite Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Azure SQL Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

# DATABASES = {
#     'default': {
#         'ENGINE': 'mssql',
#         'NAME': config("SQL_NAME", ""),
#         'HOST': config("SQL_SERVER", ""),
#         'PORT': '1433',
#         'USER': config("SQL_USER",""),
#         'PASSWORD': config("SQL_PASSWORD",""),
#         'OPTIONS': {
# 	            'driver': config('SQL_DRIVER', ""),
#                 'timeout': 600,
# 	        },
#         'CONN_HEALTH_CHECKS': True,
#     }
# }


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

# Added by me
#TIME_ZONE = 'UTC'
TIME_ZONE = 'Asia/Kuala_Lumpur'

USE_I18N = True

# Added by me.
# USE_TZ = False when using Azure SQL
#USE_TZ = True
USE_TZ = False


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

STATICFILES_DIRS = [
    BASE_DIR / "static",
    BASE_DIR / "hello" / "static",
]

STATIC_URL = "static/"
STATIC_ROOT = BASE_DIR / "staticfiles"

# MEDIA_ROOT: Absolute filesystem path to the directory that will hold user-uploaded files.
MEDIA_URL = "media/"
# Default MEDIA_ROOT
#MEDIA_ROOT = BASE_DIR / "media"
MEDIA_ROOT = BASE_DIR.parent / "outside_file_holder/RiffMates/uploads/"

# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Static file serving.
# https://whitenoise.readthedocs.io/en/stable/django.html#add-compression-and-caching-support
STORAGES = {
    # ...
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    },
    "default": {
        "BACKEND": "django.core.files.storage.FileSystemStorage",
    },
}

# Setting where to redirect users to if there is no next
# argument provided to the login page.
# Where to redirect to when the user logs out.
# Account management
LOGIN_REDIRECT_URL = '/bands/bands/'
#LOGOUT_REDIRECT_URL = '/accounts/logout/'
# For resetting password
# With Django default email backed
#EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# Azure email backend
# https://pypi.org/project/django-azure-communication-email/
# Now, when you use django.core.mail.send_mail, Azure 
# Communication Email service will send the messages by default.
EMAIL_BACKEND = 'django_azure_communication_email.EmailBackend'
AZURE_KEY_CREDENTIAL = config("AZURE_COMM_KEY", "")
AZURE_COMMUNICATION_ENDPOINT = config("AZURE_COMM_ENDPOINT", "")
DEFAULT_FROM_EMAIL="<DoNotReply@f0cf672a-d027-4901-bfea-018e517e7e1c.azurecomm.net>"

# For form templates
#class CustomFormRenderer(TemplatesSetting):
#    form_template_name = "form_template.html"

#FORM_RENDER = "hello.settings.CustomFormRenderer"
