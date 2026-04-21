from django.apps import AppConfig


class CoreConfig(AppConfig):
    """
    Menyimpan konfigurasi dasar modul inti aplikasi.

    Modul ini menaungi kebutuhan umum seperti sistem pencatatan (logging),
    hak akses admin, middleware, dan penanganan galat secara global.
    """
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'core'

    def ready(self):
        """
        Menjalankan inisialisasi awal saat aplikasi mulai dimuat.

        Fungsi ini turut menyematkan perbaikan tambahan secara otomatis 
        agar sistem dasbor tetap stabil dan berjalan lancar.
        """
        self._patch_unfold_context_bug()

    def _patch_unfold_context_bug(self):
        """
        Memperbaiki kendala pemuatan data pada tampilan dasbor secara dinamis.

        Fungsi ini menambal kode pustaka eksternal secara halus saat aplikasi
        berjalan, guna mencegah galat pada operasi pengelolaan data.
        """
        try:
            import unfold.templatetags.unfold as unfold_tags
            
            def patched_flatten_context(context):
                """
                Menyusun ulang data dari objek context secara aman.
                """
                try:
                    return context.flatten()
                except ValueError:
                    def get_keys(ctx):
                        keys = set()
                        for d in getattr(ctx, 'dicts', []):
                            if hasattr(d, 'keys'):
                                keys.update(d.keys())
                            elif hasattr(d, 'dicts'):
                                keys.update(get_keys(d))
                        return keys
                    
                    flat = {}
                    for k in get_keys(context):
                        try:
                            flat[k] = context[k]
                        except KeyError:
                            pass
                    return flat

            unfold_tags._flatten_context = patched_flatten_context
        except ImportError:
            pass