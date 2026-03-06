from .base import *
import os

SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY', default='p5bmz^gv6a9z)&w#8q^kkbbq$lgp^)ub^0ps6knu%&(wxnz7z')

DEBUG = False

ALLOWED_HOSTS = os.environ.get('DJANGO_ALLOWED_HOSTS', 'ngekost.biz.id,www.ngekost.biz.id').split(',')

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

CORS_ALLOWED_ORIGINS = [
    "https://ngekost.biz.id",
    "https://www.ngekost.biz.id",
]

SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
X_FRAME_OPTIONS = 'DENY'