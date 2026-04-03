from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Kost(models.Model):
    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='kosts',
        verbose_name='Pemilik Kost',
        help_text='Pengguna owner yang bertanggung jawab atas data kost ini.',
    )
    name = models.CharField(
        max_length=255,
        verbose_name='Nama Kost',
        help_text='Nama properti kost yang akan ditampilkan kepada calon tenant.',
    )
    address = models.TextField(
        verbose_name='Alamat',
        help_text='Alamat lengkap kost agar mudah ditemukan oleh tenant dan admin.',
    )
    description = models.TextField(
        verbose_name='Deskripsi',
        help_text='Ringkasan kondisi, keunggulan, dan informasi penting mengenai kost.',
    )
    facilities = models.TextField(
        verbose_name='Fasilitas',
        help_text='Daftar fasilitas kost. Pisahkan dengan koma, misalnya: WiFi, AC, Kamar Mandi Dalam.',
    )
    latitude = models.DecimalField(
        max_digits=9,
        decimal_places=6,
        null=True,
        blank=True,
        verbose_name='Latitude',
        help_text='Koordinat lintang lokasi kost. Opsional, digunakan untuk kebutuhan pemetaan.',
    )
    longitude = models.DecimalField(
        max_digits=9,
        decimal_places=6,
        null=True,
        blank=True,
        verbose_name='Longitude',
        help_text='Koordinat bujur lokasi kost. Opsional, digunakan untuk kebutuhan pemetaan.',
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Dibuat Pada',
        help_text='Waktu saat data kost pertama kali dibuat.',
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='Diperbarui Pada',
        help_text='Waktu terakhir data kost diperbarui.',
    )

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Kost'
        verbose_name_plural = 'Daftar Kost'

    def __str__(self):
        return f"{self.name} - {self.owner.username}"
    

class Room(models.Model):
    STATUS_CHOICES = (
        ('available', 'Tersedia'),
        ('booked', 'Dipesan'),
        ('occupied', 'Dihuni'),
    )

    kost = models.ForeignKey(
        Kost,
        on_delete=models.CASCADE,
        related_name='rooms',
        verbose_name='Kost',
        help_text='Kost induk tempat kamar ini terdaftar.',
    )
    room_number = models.CharField(
        max_length=50,
        verbose_name='Nomor Kamar',
        help_text='Nomor atau kode unik kamar dalam satu kost.',
    )
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name='Harga per Bulan',
        help_text='Harga sewa kamar per bulan sesuai penawaran owner.',
    )
    status = models.CharField(
        max_length=15,
        choices=STATUS_CHOICES,
        default='available',
        verbose_name='Status Kamar',
        help_text='Status operasional kamar: tersedia, dipesan, atau sudah dihuni.',
    )
    description = models.TextField(
        blank=True,
        null=True,
        verbose_name='Deskripsi Kamar',
        help_text='Catatan tambahan mengenai ukuran, fasilitas, atau kondisi kamar.',
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Dibuat Pada',
        help_text='Waktu saat data kamar pertama kali dibuat.',
    )

    class Meta:
        ordering = ['price']
        unique_together = ('kost', 'room_number')
        verbose_name = 'Kamar'
        verbose_name_plural = 'Daftar Kamar'

    def __str__(self):
        return f"Kamar {self.room_number} - {self.kost.name}"