from django.db.models import Count
from users.models import CustomUser
from kosts.models import Kost, Room
from transactions.models import Booking

def dashboard_callback(request, context):
    """
    Menyiapkan data statistik untuk ditampilkan di halaman utama dasbor.

    Fungsi ini menghitung metrik penting seperti total pengguna, kost, kamar, 
    serta transaksi, lalu menyisipkannya ke dalam antarmuka admin.

    Args:
        request (HttpRequest): Objek request yang memuat informasi klien.
        context (dict): Data yang akan diproses dan dirender oleh halaman dasbor.

    Returns:
        dict: Mengembalikan konteks yang diperbarui dengan statistik ringkas.
    """
    total_users = CustomUser.objects.count()
    total_kosts = Kost.objects.count()
    total_rooms = Room.objects.count()
    total_bookings = Booking.objects.count()
    pending_verifications = Booking.objects.filter(status='waiting_verification').count()
    
    kpi = [
        {
            "title": "Total Pengguna",
            "metric": f"{total_users:,}",
            "footer": "Semua pengguna terdaftar",
        },
        {
            "title": "Total Kost",
            "metric": f"{total_kosts:,}",
            "footer": "Properti yang dikelola",
        },
        {
            "title": "Total Kamar",
            "metric": f"{total_rooms:,}",
            "footer": "Kamar tersedia & disewa",
        },
        {
            "title": "Total Booking",
            "metric": f"{total_bookings:,}",
            "footer": "Keseluruhan transaksi",
        },
        {
            "title": "Menunggu Verifikasi",
            "metric": f"{pending_verifications:,}",
            "footer": "Butuh tindakan segera",
        },
    ]

    context.update({
        "kpi": kpi,
    })
    return context