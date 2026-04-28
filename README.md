# Ngekost.id Backend API

Ngekost.id adalah platform marketplace kost modern yang dirancang untuk mempermudah proses pencarian, pemesanan, dan pengelolaan properti kost secara digital. Repository ini berisi layanan backend berbasis REST API yang menangani seluruh logika bisnis utama aplikasi.

## Fitur Utama

- **Autentikasi & Otorisasi:** Sistem keamanan menggunakan JWT (JSON Web Token) dengan pembagian peran pengguna (**Admin**, **Owner**, dan **Tenant**).
- **Sistem Metode Pembayaran:** Pemilik kost dapat mengelola opsi pembayaran seperti **QRIS** atau transfer bank untuk memudahkan tenant sebelum transaksi.
- **Admin Panel Profesional:** Monitoring data terpusat menggunakan antarmuka admin yang elegan dan responsif.
- **Dokumentasi API:** Dokumentasi interaktif yang memudahkan integrasi dengan frontend (Next.js/Flutter).
- **Verifikasi Pembayaran:** Alur unggah bukti transfer oleh tenant yang dapat disetujui atau ditolak secara langsung oleh pemilik kost.

## Teknologi Utama

- **API Documentation:** Drf-spectacular (OpenAPI 3.0)
- **Framework:** Django 5.0 & Django REST Framework
- **Autentikasi:** SimpleJWT (OAuth2 style)
- **Database:** SQLite (Dev) / MySQL (Prod)
- **Media Handling:** Pillow

## Instalasi

1. **Clone Repository**
   
   ```bash
   git clone https://github.com/0xPutri/Ngekost.id_Backend.git
   cd Ngekost.id_Backend
   ```

2. **Persiapkan Lingkungan (Venv)**
   
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/macOS
   # venv\Scripts\activate   # Windows
   ```

3. **Instal Dependensi**
   
   ```bash
   pip install -r requirements.txt
   cp .env.example .env
   ```

4. **Konfigurasi Database**
   
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

5. **Jalankan Server**
   
   ```bash
   python manage.py runserver
   ```

## Dokumentasi API

Setelah server berjalan, Anda dapat mengakses dokumentasi API pada endpoint berikut:

- **Swagger UI:** `/api/docs/` (Rekomendasi)
- **ReDoc:** `/api/redoc/`
- **Schema:** `/api/schema/`

## Admin Panel

Aplikasi ini menggunakan **Django Unfold** untuk menyediakan pengalaman administratif yang elegan dan profesional. Admin panel dapat diakses melalui:

- **URL:** `/admin/`
- **Fitur:** Dashboard statistik, manajemen pengguna multi-role, audit log properti, dan verifikasi transaksi.

## Catatan

- **Keamanan:** Selalu gunakan file `.env` untuk menyimpan informasi sensitif seperti `SECRET_KEY`, kredensial database, dan API key.
- **Database:** Pastikan untuk menjalankan `makemigrations` dan `migrate` setiap kali ada perubahan pada struktur model di `kosts/models.py`.
- **Admin Panel:** Akun Superuser dapat dibuat menggunakan perintah `python manage.py createsuperuser` untuk mengakses dashboard admin di `/admin/`.

## Lisensi

Proyek ini menggunakan lisensi **MIT**. Lihat detail lengkap pada file [`LICENSE`](LICENSE).