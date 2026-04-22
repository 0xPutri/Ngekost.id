from django.contrib import admin
from unfold.admin import ModelAdmin
from core.admin_mixins import RoleBasedModelAdminMixin
from .models import Booking, PaymentProof
from kosts.models import Room

@admin.register(Booking)
class BookingAdmin(RoleBasedModelAdminMixin, ModelAdmin):
    """
    Menata tampilan daftar riwayat pemesanan pada panel admin Dasbor.

    Pengaturan ini mempermudah admin dalam memantau status pesanan, menelusuri 
    transaksi penyewa, dan memeriksa detail kamar secara cepat.
    """
    owner_field_path = 'room__kost__owner'
    list_display = ('id', 'tenant', 'room', 'status', 'total_price', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('tenant__username', 'room__room_number', 'room__kost__name')
    list_display_links = ('id', 'tenant')

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "room" and getattr(request.user, 'role', None) == 'owner':
            kwargs["queryset"] = Room.objects.filter(kost__owner=request.user)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

@admin.register(PaymentProof)
class PaymentProofAdmin(RoleBasedModelAdminMixin, ModelAdmin):
    """
    Menata tampilan daftar bukti pembayaran pada panel admin Dasbor.

    Pengaturan ini membantu admin dalam memvalidasi berkas pembayaran
    yang diunggah oleh penyewa secara praktis.
    """
    owner_field_path = 'booking__room__kost__owner'
    list_display = ('id', 'booking', 'uploaded_at')
    search_fields = ('booking__tenant__username', 'booking__id')
    list_display_links = ('id', 'booking')

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "booking" and getattr(request.user, 'role', None) == 'owner':
            kwargs["queryset"] = Booking.objects.filter(room__kost__owner=request.user)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)