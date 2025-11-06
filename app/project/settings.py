import os
import pymysql
from pathlib import Path
import environ
env = environ.Env()
environ.Env.read_env()

BASE_DIR = Path(__file__).resolve().parent.parent

pymysql.install_as_MySQLdb()

DEBUG = True
LOAD_DEBUG_TOOLBAR = False

if DEBUG:
    env.read_env(os.path.join(os.path.dirname(os.path.abspath(__file__)), '.env_testing'))
else:
    env.read_env(os.path.join(os.path.dirname(os.path.abspath(__file__)), '.env_production'))

SECRET_KEY = env('PROJECT_SECRET_KEY')

SITE_ID = 1

ALLOWED_HOSTS = ["*"]

INSTALLED_APPS = [
    'django_crontab',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework.authtoken',
    'django.contrib.sitemaps',
    'django.contrib.humanize',
    'rest_framework',
    'django_db_logger',
    'django_cleanup.apps.CleanupConfig',
    'drf_yasg',
    'accounts',
    'frontend',
    'logger',
    'users',
    'static_pages',
    'backup',
    'contact_us',
    'credentials',
    'wardrobe',
    'subscription',
    'ecommerce',
    "debug_toolbar",
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    # 'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware',
]

ROOT_URLCONF = 'project.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
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

WSGI_APPLICATION = 'project.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': env('DB_ENGINE'),
        'NAME': env('DB_NAME'),
        'USER': env('DB_USER'),
        'PASSWORD': env('DB_PASSWORD'),
        'HOST': env('DB_HOST'),
        'PORT': env('DB_PORT'),
        'CONN_MAX_AGE': 600,
        'OPTIONS': {'charset': 'utf8mb4'},
    }
}

AUTHENTICATION_BACKENDS = ['accounts.backend.EmailLoginBackend']

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

# CRONJOBS = [
#     ('0 0 * * 7', 'accounts.cron.WeeklyDataBaseBackup'),
#     ('0 0 */10 * *', 'accounts.cron.DeleteUnnecessaryData'),
# ]

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_X_FORWARDED_HOST = True

USE_L10N = True

USE_TZ = False

AUTH_USER_MODEL = "accounts.User"



STATIC_URL = '/static/'
if not DEBUG:
    STATICFILES_DIRS = (
        os.path.join(BASE_DIR, "static", "admin-assets"),
    )
    STATIC_ROOT = os.path.join(BASE_DIR, 'static')
else:
    STATICFILES_DIRS = (
        os.path.join(BASE_DIR, "static", "admin-assets"),
        os.path.join(BASE_DIR, 'static'),
    )
MEDIA_URL = '/media/'
MEDIA_ROOT = (os.path.join(BASE_DIR, 'media'))


## Rest API's Authentication Settings
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
       'rest_framework.authentication.TokenAuthentication',
    ),
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 10
}

## Swagger Settings
SWAGGER_SETTINGS = {
    'JSON_EDITOR': True,
    'SECURITY_DEFINITIONS': {
        'Bearer': {
            'type': 'apiKey',
            'name': 'Authorization',
            'in': 'header'
        }
    },
    'PERSIST_AUTH': True
}

## Db Logger Settings
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s'
        },
        'simple': {
            'format': '%(levelname)s %(asctime)s %(message)s'
        },
    },
    'handlers': {
        'db_log': {
            'level': 'DEBUG',
            'class': 'django_db_logger.db_log_handler.DatabaseLogHandler'
        },
    },
    'loggers': {
        'db': {
            'handlers': ['db_log'],
            'level': 'DEBUG'
        },
        'django.request': {
            'handlers': ['db_log'],
            'level': 'ERROR',
            'propagate': False,
        }
    }
}

## Custom SMTP settings
EMAIL_BACKEND = 'credentials.smtp.CustomEmailBackend'
EMAIL_USE_TLS = True  
EMAIL_HOST = env('EMAIL_HOST')
EMAIL_PORT = env('EMAIL_PORT')
EMAIL_HOST_USER = env('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = env('EMAIL_HOST_PASSWORD')
SERVER_EMAIL = EMAIL_HOST_USER
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER

## REDIS & CELERY & CELERY CRONTAB SETTING 
# INSTALLED_APPS += [
#     'django_celery_beat',
# ]

# from celery.schedules import crontab
# CELERY_BEAT_SCHEDULE = {
#     "weekly_backup": {
#         "task": "accounts.cron.WeeklyDataBaseBackup",
#         "schedule": crontab(minute=0, hour=0, day_of_week=0),  # Sunday
#     },
#     "delete_old_data": {
#         "task": "accounts.cron.DeleteUnnecessaryData",
#         "schedule": crontab(minute=0, hour=0, day_of_month='*/10'),
#     },
# }
# CELERY_TIMEZONE = 'UTC'
# CELERY_ENABLE_UTC = True
# CELERY_BROKER_URL = 'redis://redis:6379/0'
# CELERY_RESULT_BACKEND = 'django-db'
# CELERY_BROKER_URL = 'redis://localhost:6379/0'
# CELERY_RESULT_BACKEND = 'django-db'
# CELERY_RESULT_BACKEND = 'django-cache'

# CELERY_CACHE_BACKEND = 'default'

# # django setting.
# CACHES = {
#     'default': {
#         'BACKEND': 'django.core.cache.backends.db.DatabaseCache',
#         'LOCATION': 'my_cache_table',
#     }
# }

# CELERY_RESULT_EXTENDED = True

## Django Debug Toolbar
# if LOAD_DEBUG_TOOLBAR:
#     INSTALLED_APPS += ['debug_toolbar']
#     MIDDLEWARE = ['debug_toolbar.middleware.DebugToolbarMiddleware'] + MIDDLEWARE
#     INTERNAL_IPS = ['127.0.0.1', 'localhost']
#     import mimetypes
#     mimetypes.add_type("application/javascript", ".js", True)