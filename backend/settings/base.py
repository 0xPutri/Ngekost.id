from datetime import timedelta
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent

# Application definition
INSTALLED_APPS = [
    'unfold',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Third-party Apps
    'rest_framework',
    'rest_framework_simplejwt',
    'corsheaders',
    'django_filters',
    'drf_spectacular',

    # Local Apps
    'core',
    'users',
    'kosts',
    'transactions',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'corsheaders.middleware.CorsMiddleware', # CORS Middleware
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'core.middleware.RequestContextLoggingMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'backend.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
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

WSGI_APPLICATION = 'backend.wsgi.application'

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# Internationalization
LANGUAGE_CODE = 'id'
TIME_ZONE = 'Asia/Jakarta'
USE_I18N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'

# Media files
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Custom User Model
AUTH_USER_MODEL = 'users.CustomUser'

# Django REST Framework Global Settings
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 10, # Paginasi default untuk mencegah overhead database
    'DEFAULT_FILTER_BACKENDS': ['django_filters.rest_framework.DjangoFilterBackend'],
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema', # Integrasi OpenAPI
    'EXCEPTION_HANDLER': 'core.exceptions.custom_exception_handler',
}

# Metadata Dokumentasi Swagger
SPECTACULAR_SETTINGS = {
    'TITLE': 'Ngekost.id API',
    'DESCRIPTION': (
        'Dokumentasi REST API untuk platform marketplace kost Ngekost.id. '
        'API ini mendukung alur registrasi dan autentikasi pengguna, pengelolaan '
        'properti kost dan kamar oleh pemilik, proses booking oleh tenant, '
        'unggah bukti pembayaran, verifikasi pembayaran oleh owner, serta '
        'monitoring operasional oleh administrator.\n\n'
        'Autentikasi menggunakan JWT Bearer Token. Untuk endpoint yang membutuhkan '
        'otorisasi, klik tombol "Authorize" di Swagger UI lalu masukkan token dengan '
        'format: `Bearer <access_token>`.'
    ),
    'VERSION': '1.0.0',
    'SERVE_INCLUDE_SCHEMA': False,
    'COMPONENT_SPLIT_REQUEST': True,
    'SCHEMA_PATH_PREFIX': r'/api/v1',
    'TAGS': [
        {
            'name': 'Autentikasi',
            'description': 'Endpoint untuk registrasi akun tenant, login JWT, dan refresh access token.',
        },
        {
            'name': 'Profil Pengguna',
            'description': 'Endpoint untuk melihat dan memperbarui profil pengguna yang sedang login.',
        },
        {
            'name': 'Kost',
            'description': 'Endpoint katalog dan pengelolaan properti kost.',
        },
        {
            'name': 'Kamar',
            'description': 'Endpoint katalog dan pengelolaan kamar pada sebuah kost.',
        },
        {
            'name': 'Booking',
            'description': 'Endpoint transaksi pemesanan kamar dan pelacakan status booking.',
        },
        {
            'name': 'Pembayaran',
            'description': 'Endpoint unggah bukti pembayaran dan verifikasi oleh pemilik kost.',
        },
        {
            'name': 'Admin Panel',
            'description': 'Endpoint administratif untuk pengawasan pengguna, kost, dan booking.',
        },
    ],
    'SWAGGER_UI_SETTINGS': {
        'deepLinking': True,
        'displayRequestDuration': True,
        'persistAuthorization': True,
        'filter': True,
        'tagsSorter': 'alpha',
        'operationsSorter': 'alpha',
        'docExpansion': 'list',
    },
}

# Simple JWT Configuration
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=60),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),
    'ROTATE_REFRESH_TOKENS': True,
    'BLACKLIST_AFTER_ROTATION': True,
    'AUTH_HEADER_TYPES': ('Bearer',),
}

# Logging Configuration
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'request_context': {
            '()': 'core.logging.RequestContextFilter',
        },
    },
    'formatters': {
        'verbose_aman': {
            '()': 'core.logging.SafeExtraFormatter',
            'format': (
                '[%(asctime)s] %(levelname)s %(name)s | pesan="%(message)s" | '
                'request_id=%(request_id)s | metode=%(http_method)s | path=%(request_path)s | '
                'user_id=%(user_id)s | peran=%(user_role)s | ip=%(client_ip)s | detail=%(extra_data)s'
            ),
            'datefmt': '%Y-%m-%d %H:%M:%S',
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'filters': ['request_context'],
            'formatter': 'verbose_aman',
        },
    },
    'loggers': {
        'ngekost': {
            'handlers': ['console'],
            'level': os.environ.get('DJANGO_LOG_LEVEL', 'INFO'),
            'propagate': False,
        },
        'django.request': {
            'handlers': ['console'],
            'level': 'WARNING',
            'propagate': False,
        },
        'django.security': {
            'handlers': ['console'],
            'level': 'WARNING',
            'propagate': False,
        },
    },
}
# Unfold Admin Configuration
UNFOLD = {
    "SITE_TITLE": "Ngekost.id Workspace",
    "SITE_HEADER": "Ngekost.id",
    "SITE_URL": "/",
    "SITE_SYMBOL": "villa",
    "DASHBOARD_CALLBACK": "core.dashboard.dashboard_callback",
    "COLORS": {
        "primary": {
            "50": "249 250 251",
            "100": "243 244 246",
            "200": "229 231 235",
            "300": "209 213 219",
            "400": "156 163 175",
            "500": "107 114 128",
            "600": "75 85 99",
            "700": "55 65 81",
            "800": "31 41 55",
            "900": "17 24 39",
            "950": "3 7 18",
        },
    },
    "SIDEBAR": {
        "show_search": True,
        "show_all_applications": False,
        "navigation": [
            {
                "title": "Dashboard",
                "separator": True,
                "items": [
                    {
                        "title": "Overview",
                        "icon": "dashboard",
                        "link": "/admin/",
                    },
                ],
            },
            {
                "title": "Master Data",
                "separator": True,
                "items": [
                    {
                        "title": "Pengguna",
                        "icon": "people",
                        "link": "/admin/users/customuser/",
                    },
                    {
                        "title": "Kost",
                        "icon": "holiday_village",
                        "link": "/admin/kosts/kost/",
                    },
                    {
                        "title": "Kamar",
                        "icon": "bed",
                        "link": "/admin/kosts/room/",
                    },
                ],
            },
            {
                "title": "Transaksi",
                "separator": True,
                "items": [
                    {
                        "title": "Metode Pembayaran",
                        "icon": "account_balance_wallet",
                        "link": "/admin/kosts/paymentmethod/",
                    },
                    {
                        "title": "Booking",
                        "icon": "receipt_long",
                        "link": "/admin/transactions/booking/",
                    },
                    {
                        "title": "Bukti Pembayaran",
                        "icon": "payments",
                        "link": "/admin/transactions/paymentproof/",
                    },
                ],
            },
            {
                "title": "Media & Galeri",
                "separator": True,
                "items": [
                    {
                        "title": "Gambar Kost",
                        "icon": "image",
                        "link": "/admin/kosts/kostimage/",
                    },
                    {
                        "title": "Gambar Kamar",
                        "icon": "photo_library",
                        "link": "/admin/kosts/roomimage/",
                    },
                ],
            },
        ],
    },
    "TABS": [
        {
            "models": [
                "users.customuser",
            ],
            "items": [
                {
                    "title": "Users",
                    "link": "/admin/users/customuser/",
                    "icon": "people",
                },
            ],
        },
    ],
}