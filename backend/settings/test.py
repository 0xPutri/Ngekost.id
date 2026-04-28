from .base import *

SECRET_KEY = 'django-insecure-test-key-for-pytest-industry-standard'
DEBUG = True

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3.test',
    }
}

PASSWORD_HASHERS = [
    'django.contrib.auth.hashers.MD5PasswordHasher',
]

LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
}