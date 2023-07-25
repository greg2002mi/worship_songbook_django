
"""
Django settings for church project.

Generated by 'django-admin startproject' using Django 4.2.3.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""
import environ, os

env=environ.Env()
environ.Env.read_env()

# gettext windows 10
os.environ.setdefault("PATH", "")  # Prevent potential issues with missing PATH variable
os.environ["PATH"] += os.pathsep + r'C:\Program Files\gettext-iconv\bin'


from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
TEMPLATE_DIR = os.path.join(BASE_DIR,'templates')
LOGIN_REDIRECT_URL = 'index'


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-qn()t8nwpor6%ouh1et45_y%i2hkjs)taa+gtb%6m%tvnzv%_j'

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
    # 'songbook',
    'songbook.apps.SongbookConfig',
    'songbook.templatetags',
    'import_export',
    'crispy_forms',
    'crispy_bootstrap4',
    'bootstrap4',
    'phonenumber_field',
    'audiofield',
    'celery',
    'django_flatpickr',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'audiofield.middleware.threadlocals.ThreadLocals',
    
]

ROOT_URLCONF = 'church.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [TEMPLATE_DIR],
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

CRISPY_TEMPLATE_PACK = 'bootstrap4'

#libraries to load custom tags
OPTIONS = {
    "libraries": {
        "templatetags": "songbook.templatetags",
        "admin.urls": "django.contrib.admin.templatetags.admin_urls",
    },
    "builtins": ["myapp.builtins"],
}

WSGI_APPLICATION = 'church.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': env("DB_NAME"), 
        'USER': env("DB_USER"),
        'PASSWORD': env("DB_PASSWORD"),
        'HOST': env("DB_HOST"), 
        'PORT': env("DB_PORT"),
    }
}

# import-export
IMPORT_EXPORT_USE_TRANSACTIONS = True

# Celery
CELERY_RESULT_BACKEND = 'django-db'
CELERY_RESULT_BACKEND_DB = ''.join(['postgresql+psycopg2://', os.getenv("DB_USER"), ":", os.getenv("DB_PASSWORD"), "@localhost/", os.getenv("DB_NAME")]) 
CELERY_CACHE_BACKEND = 'django-cache' 
## Broker settings.
CELERY_BROKER_URL = 'redis://localhost:6379' 
CELERY_ACCEPT_CONTENT = ['application/json'] 
CELERY_TASK_SERIALIZER = 'json' 
CELERY_RESULT_SERIALIZER = 'json' 

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

# if to use AbstractUser to add additional fields to default User
# AUTH_USER_MODEL = 'songbook.CustomUser'

# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'en'

LANGUAGES = (
    ("en", "US English"),
    ("ko", "Korean"),
    ("ru", "Russian"),
    
)

# PHONENUMBER_DEFAULT_REGION = 'KR'

LOCALE_PATHS = [
    os.path.join(BASE_DIR, 'locale'),
    os.path.join(BASE_DIR, 'songbook', 'locale'),
]

# pagination
PAGE_SIZE = 100

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Mailing system
SENDGRID_API_KEY = os.getenv('SENDGRID_API_KEY')

EMAIL_HOST = 'smtp.sendgrid.net'
EMAIL_HOST_USER = 'apikey' # this is exactly the value 'apikey'
EMAIL_HOST_PASSWORD = SENDGRID_API_KEY
EMAIL_PORT = 587
EMAIL_USE_TLS = True

EMAIL_BACKEND = "sendgrid_backend.SendgridBackend"
SENDGRID_API_KEY = os.environ["SENDGRID_API_KEY"]
EMAIL_FILE_PATH = BASE_DIR / "sent_emails"

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = 'static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

# Frontend widget values
# 0-Keep original, 1-Mono, 2-Stereo
CHANNEL_TYPE_VALUE = 0

# 0-Keep original, 8000-8000Hz, 16000-16000Hz, 22050-22050Hz,
# 44100-44100Hz, 48000-48000Hz, 96000-96000Hz
FREQ_TYPE_VALUE = 8000

# 0-Keep original, 1-Convert to MP3, 2-Convert to WAV, 3-Convert to OGG
CONVERT_TYPE_VALUE = 0

MEDIA_ROOT = os.path.join(BASE_DIR, 'songbook/media')
MEDIA_URL = "/songbook/media/"

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

DATA_UPLOAD_MAX_MEMORY_SIZE = 15728640

FILE_UPLOAD_MAX_MEMORY_SIZE = 15728640

# FILE_UPLOAD_HANDLERS = [
#     "django.core.files.uploadhandler.MemoryFileUploadHandler",
#     "django.core.files.uploadhandler.TemporaryFileUploadHandler",
# ]