from django.apps import AppConfig


class CoreConfig(AppConfig):
    """
    Menyimpan konfigurasi dasar modul inti aplikasi.

    Modul ini menaungi kebutuhan umum seperti logging, permission admin,
    middleware, dan penanganan galat global.
    """
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'core'