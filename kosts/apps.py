from django.apps import AppConfig


class KostsConfig(AppConfig):
    """
    Menyimpan konfigurasi dasar aplikasi kost dan kamar.

    Konfigurasi ini membantu Django memuat modul pengelolaan properti
    marketplace kost dalam proyek Ngekost.id.
    """
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'kosts'