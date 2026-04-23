from .base import *
import os
from django.core.exceptions import ImproperlyConfigured

SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY')
if not SECRET_KEY:
    raise ImproperlyConfigured("DJANGO_SECRET_KEY harus dikonfigurasi pada environment production.")

DEBUG = False

allowed_hosts = os.environ.get('DJANGO_ALLOWED_HOSTS')
if not allowed_hosts:
    raise ImproperlyConfigured("DJANGO_ALLOWED_HOSTS harus dikonfigurasi pada environment production.")

ALLOWED_HOSTS = [host.strip() for host in allowed_hosts.split(',') if host.strip()]
ENABLE_DJANGO_ADMIN = os.environ.get('ENABLE_DJANGO_ADMIN', 'False').lower() == 'true'

cors_allowed_origins = os.environ.get('DJANGO_CORS_ALLOWED_ORIGINS')
if not cors_allowed_origins:
    raise ImproperlyConfigured(
        "DJANGO_CORS_ALLOWED_ORIGINS harus dikonfigurasi pada environment production."
    )

CORS_ALLOWED_ORIGINS = [
    origin.strip()
    for origin in cors_allowed_origins.split(',')
    if origin.strip()
]

# Database Configuration (MySQL Online)
DATABASES = {
    'default': {
        'ENGINE': os.environ.get('DB_ENGINE', 'django.db.backends.mysql'),
        'NAME': os.environ.get('DB_NAME', 'ngekost_db'),
        'USER': os.environ.get('DB_USER'),
        'PASSWORD': os.environ.get('DB_PASSWORD'),
        'HOST': os.environ.get('DB_HOST'),
        'PORT': os.environ.get('DB_PORT', '3306'),
        'OPTIONS': {
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
            'charset': 'utf8mb4',
        }
    }
}

SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
X_FRAME_OPTIONS = 'DENY'