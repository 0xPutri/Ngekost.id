from django.apps import AppConfig


class TransactionsConfig(AppConfig):
    """
    Menyimpan konfigurasi dasar aplikasi transaksi.

    Konfigurasi ini membantu Django mengenali modul booking dan pembayaran
    sebagai bagian dari proyek Ngekost.id.
    """
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'transactions'