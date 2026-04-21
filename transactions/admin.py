from django.contrib import admin
from unfold.admin import ModelAdmin
from .models import Booking, PaymentProof

@admin.register(Booking)
class BookingAdmin(ModelAdmin):
    """
    Menata tampilan daftar riwayat pemesanan pada panel admin Dasbor.

    Pengaturan ini mempermudah admin dalam memantau status pesanan, menelusuri 
    transaksi penyewa, dan memeriksa detail kamar secara cepat.
    """
    list_display = ('id', 'tenant', 'room', 'status', 'total_price', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('tenant__username', 'room__room_number', 'room__kost__name')
    list_display_links = ('id', 'tenant')

@admin.register(PaymentProof)
class PaymentProofAdmin(ModelAdmin):
    """
    Menata tampilan daftar bukti pembayaran pada panel admin Dasbor.

    Pengaturan ini membantu admin dalam memvalidasi berkas pembayaran
    yang diunggah oleh penyewa secara praktis.
    """
    list_display = ('id', 'booking', 'uploaded_at')
    search_fields = ('booking__tenant__username', 'booking__id')
    list_display_links = ('id', 'booking')