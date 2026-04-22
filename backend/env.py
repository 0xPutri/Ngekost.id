from pathlib import Path
from dotenv import load_dotenv


def load_environment() -> None:
    """
    Memuat variabel environment proyek dari file `.env`.

    Fungsi ini membantu backend membaca konfigurasi lokal secara konsisten
    sebelum Django menginisialisasi pengaturannya.
    """
    project_root = Path(__file__).resolve().parent.parent
    load_dotenv(project_root / '.env')