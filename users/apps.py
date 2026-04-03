from django.apps import AppConfig


class UsersConfig(AppConfig):
    """
    Menyimpan konfigurasi dasar aplikasi pengguna.

    Konfigurasi ini membantu Django mengenali modul autentikasi dan profil
    sebagai bagian dari proyek Ngekost.id.
    """
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'users'