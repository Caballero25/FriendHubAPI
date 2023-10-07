from .base import *

DEBUG = True

ALLOWED_HOSTS = []

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': secret_data["DB_NAME"],
        'USER': secret_data["DB_USER"],
        'PASSWORD': secret_data["DB_PASSWORD"],
        'HOST': 'localhost',
        'PORT': '5432'
    }
}


STATIC_URL = 'static/'

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
