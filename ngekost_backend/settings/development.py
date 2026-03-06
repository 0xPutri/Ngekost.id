from .base import *

SECRET_KEY = 'p5bmz^gv6a9z)&w#8q^kkbbq$lgp^)ub^0ps6knu%&(wxnz7z'

DEBUG = True

ALLOWED_HOSTS = ['localhost', '127.0.0.1']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# CORS configuration for local frontend development (Next.js / Flutter Web)
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]