#!/usr/bin/env python
"""Menyediakan utilitas baris perintah untuk pengelolaan proyek Django."""
import sys
import os
from ngekost_backend.env import load_environment


def main():
    """
    Menjalankan perintah administratif untuk proyek Ngekost.id.

    Fungsi ini memuat environment proyek lebih dulu agar pengaturan Django
    dapat dibaca dengan konsisten pada setiap perintah manajemen.
    """
    load_environment()
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ngekost_backend.settings.development')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()