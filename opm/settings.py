"""
Django settings for opm project.

Generated by 'django-admin startproject' using Django 4.2.13.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""
import os
from pathlib import Path
import cloudinary_storage
# import dj_database_url

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-a&b81*@0h=&035ho$$jhbvd=62abat-rh1)u17+kvtqj(jzuh4'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['.vercel.app', '.now.sh', '127.0.0.1']
# ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'jazzmin',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'opmApp',
    'cloudinary',
    'cloudinary_storage',
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

ROOT_URLCONF = 'opm.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR/ 'template'],
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

WSGI_APPLICATION = 'opm.wsgi.application'




# postgres://avnadmin:AVNS_EhBGgBs84ma2m0AW9qP@pg-4e91638-opms.l.aivencloud.com:27207/defaultdb?sslmode=require


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

# DATABASES = {
#     'default': dj_database_url.config{
#         'ENGINE': 'django_cockroachdb',
#         'NAME': BASE_DIR / 'db.sqlite3',
#     }
# }


# DATABASE_URL = "postgresql://blessing:rWEf27wCcy9ID-eLyV70Mw@opmsdatabase-15955.8nj.gcp-europe-west1.cockroachlabs.cloud:26257/defaultdb?sslmode=verify-full"

# DATABASES = {
#     'default': dj_database_url.parse(DATABASE_URL, engine='django_cockroachdb')
# }



DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'defaultdb', 
        'USER': 'avnadmin',   
        'PASSWORD': 'AVNS_EhBGgBs84ma2m0AW9qP',  
        'HOST': 'pg-4e91638-opms.l.aivencloud.com',
        'PORT': '27207',
        'OPTIONS': {
            'sslmode': 'require', 
            # 'sslrootcert': 'system',
        },
    }
}



# DATABASES = {'default': dj_database_url.config(default=os.environ['DATABASE_URL'], engine='django_cockroachdb')}


# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = 'static/'
STATICFILES_DIRS = os.path.join(BASE_DIR, 'static'),
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles_build', 'static')


# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


AUTH_USER_MODEL = 'opmApp.CustomUser'




# +================================ CODE FOR EMAIL NOTIFICAION ======================

EMAIL_BACKEND ='django.core.mail.backends.smtp.EmailBackend' # the email backend is a fixed you must put it exactly how you see it
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_USE_SSL = False
EMAIL_HOST_USER='adeblessinme4u@gmail.com' #Your email address will be here i.e the sender email address
EMAIL_HOST_PASSWORD ='qvpx txbb mrji blpz' #the Email Host Password you will put your App Password since google don't allow "less secure app", you can find or create app password in your google account by navigating to security then search for App password, then you can create or copy the password there.




AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',  # Default backend
    'opmApp.backends.PatientBackend',  # Custom backend
]



# FOR IMAGE OR FILE UPLOADING...

MEDIA_ROOT= 'static/opms'
MEDIA_URL='/opms/'


CLOUDINARY_STORAGE={
    'CLOUD_NAME': 'dbqtos6rt',
    'API_KEY': '688616267922488',
    'API_SECRET': '1vX0m1yd1ihW-8vfWkv3pep4nfw'
}

DEFAULT_FILE_STORAGE ='cloudinary_storage.storage.MediaCloudinaryStorage'



JAZZMIN_SETTINGS ={
    "site_title": "OPMS",
    "site_header": "OPMS ADMINISTRATION",
    "site_brand": "OPMS ADMINISTRATION",
    "copyright": "LUTH",
    "site_logo": "https://res.cloudinary.com/dbqtos6rt/image/upload/v1720673537/opms/assets/logo_iueamp.png",
}