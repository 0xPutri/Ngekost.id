from django.db import models
from django.contrib.auth import get_user_model
from kosts.models import Room

User = get_user_model()

class Booking(models.Model):
    """
    Menyimpan transaksi pemesanan kamar oleh tenant.

    Model ini merekam kamar yang dipesan, durasi sewa, total biaya, dan
    status alur pembayaran sampai verifikasi selesai.
    """
    STATUS_CHOICES = (
        ('pending_payment', 'Menunggu Pembayaran'),
        ('waiting_verification', 'Menunggu Verifikasi'),
        ('paid', 'Lunas'),
        ('rejected', 'Ditolak'),
    )

    tenant = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='bookings',
        verbose_name='Tenant',
        help_text='Pengguna tenant yang melakukan pemesanan kamar.',
    )
    room = models.ForeignKey(
        Room,
        on_delete=models.PROTECT,
        related_name='bookings',
        verbose_name='Kamar',
        help_text='Kamar yang dipesan dalam transaksi ini.',
    )
    start_date = models.DateField(
        verbose_name='Tanggal Mulai Sewa',
        help_text='Tanggal mulai masa sewa yang diajukan tenant.',
    )
    duration_months = models.PositiveIntegerField(
        default=1,
        verbose_name='Durasi Sewa (Bulan)',
        help_text='Lama sewa dalam satuan bulan.',
    )
    total_price = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        editable=False,
        verbose_name='Total Harga',
        help_text='Total biaya booking yang dihitung otomatis berdasarkan harga kamar dan durasi sewa.',
    )
    status = models.CharField(
        max_length=25,
        choices=STATUS_CHOICES,
        default='pending_payment',
        verbose_name='Status Booking',
        help_text='Status transaksi booking: menunggu pembayaran, verifikasi, lunas, atau ditolak.',
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Dibuat Pada',
        help_text='Waktu saat booking pertama kali dibuat.',
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='Diperbarui Pada',
        help_text='Waktu terakhir data booking diperbarui.',
    )

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Booking'
        verbose_name_plural = 'Daftar Booking'

    def __str__(self):
        """
        Mengembalikan label booking untuk kebutuhan internal sistem.

        Returns:
            str: Ringkasan booking berisi id, tenant, dan nomor kamar.
        """
        return f"Booking #{self.id} - {self.tenant.username} - {self.room.room_number}"
    
    def save(self, *args, **kwargs):
        """
        Menyimpan booking sambil menghitung total harga awal jika diperlukan.

        Args:
            *args: Argumen tambahan bawaan method `save`.
            **kwargs: Opsi tambahan bawaan method `save`.
        """
        if not self.total_price and self.room:
            self.total_price = self.room.price * self.duration_months
        super().save(*args, **kwargs)

class PaymentProof(models.Model):
    """
    Menyimpan bukti pembayaran yang diunggah tenant.

    Model ini terhubung satu-satu dengan booking agar setiap transaksi hanya
    memiliki satu bukti pembayaran aktif untuk diverifikasi owner.
    """
    booking = models.OneToOneField(
        Booking,
        on_delete=models.CASCADE,
        related_name='payment_proof',
        verbose_name='Booking',
        help_text='Booking yang terkait dengan bukti pembayaran ini.',
    )
    image = models.ImageField(
        upload_to='payments/%Y/%m/%d/',
        verbose_name='Gambar Bukti Pembayaran',
        help_text='File gambar bukti transfer atau pembayaran yang diunggah tenant.',
    )
    uploaded_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Diunggah Pada',
        help_text='Waktu saat bukti pembayaran diunggah ke sistem.',
    )

    class Meta:
        verbose_name = 'Bukti Pembayaran'
        verbose_name_plural = 'Bukti Pembayaran'

    def __str__(self):
        """
        Mengembalikan label bukti pembayaran untuk tampilan internal.

        Returns:
            str: Nama singkat bukti pembayaran berdasarkan id booking.
        """
        return f"Bukti Pembayaran - Booking #{self.booking.id}"