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

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
X_FRAME_OPTIONS = 'DENY'