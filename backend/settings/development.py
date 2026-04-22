from .base import *
import os
from django.core.exceptions import ImproperlyConfigured

SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY', default='')

DEBUG = True

ALLOWED_HOSTS = ['localhost', '127.0.0.1']
ENABLE_DJANGO_ADMIN = os.environ.get('ENABLE_DJANGO_ADMIN', 'False').lower() == 'true'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

development_cors_allowed_origins = os.environ.get(
    'DJANGO_CORS_ALLOWED_ORIGINS',
    'http://localhost:3000,http://127.0.0.1:3000',
)

CORS_ALLOWED_ORIGINS = [
    origin.strip()
    for origin in development_cors_allowed_origins.split(',')
    if origin.strip()
]