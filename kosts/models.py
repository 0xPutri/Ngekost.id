from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Kost(models.Model):
    """
    Menyimpan data properti kost yang dipublikasikan owner.

    Model ini menjadi pusat informasi kost, mulai dari alamat, fasilitas,
    deskripsi, hingga relasinya dengan kamar yang tersedia.
    """
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
        """
        Mengembalikan label kost yang mudah dikenali di tampilan internal.

        Returns:
            str: Nama kost beserta username owner.
        """
        return f"{self.name} - {self.owner.username}"
    

class Room(models.Model):
    """
    Menyimpan data kamar yang berada di dalam satu kost.

    Model ini memuat informasi harga, status ketersediaan, dan identitas
    kamar yang akan dipakai pada proses pencarian serta booking.
    """
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
        """
        Mengembalikan label kamar untuk kebutuhan admin dan debugging.

        Returns:
            str: Nomor kamar beserta nama kost induknya.
        """
        return f"Kamar {self.room_number} - {self.kost.name}"


class KostImage(models.Model):
    """
    Menyimpan file gambar yang terkait dengan sebuah kost.

    Model ini dipakai untuk mendukung kebutuhan galeri atau dokumentasi visual
    properti kost tanpa mengubah data inti kost maupun kamar.
    """
    kost = models.ForeignKey(
        Kost,
        on_delete=models.CASCADE,
        related_name='images',
        verbose_name='Kost',
        help_text='Kost yang memiliki gambar ini.',
    )
    image = models.ImageField(
        upload_to='kosts/%Y/%m/%d/',
        verbose_name='Gambar Kost',
        help_text='File gambar utama atau pendukung yang menampilkan kondisi kost.',
    )
    caption = models.CharField(
        max_length=255,
        blank=True,
        verbose_name='Keterangan Gambar',
        help_text='Keterangan singkat untuk membantu admin atau owner mengenali isi gambar.',
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Dibuat Pada',
        help_text='Waktu saat gambar kost pertama kali diunggah.',
    )

    class Meta:
        ordering = ['created_at']
        verbose_name = 'Gambar Kost'
        verbose_name_plural = 'Galeri Gambar Kost'

    def __str__(self):
        """
        Mengembalikan label gambar kost untuk kebutuhan admin dan debugging.

        Returns:
            str: Nama kost beserta identitas ringkas gambar.
        """
        if self.caption:
            return f"{self.kost.name} - {self.caption}"
        return f"{self.kost.name} - Gambar #{self.pk}"


class RoomImage(models.Model):
    """
    Menyimpan file gambar yang terkait dengan sebuah kamar.

    Model ini mendukung kebutuhan dokumentasi visual kamar agar calon tenant
    dapat melihat kondisi unit secara lebih rinci.
    """
    room = models.ForeignKey(
        Room,
        on_delete=models.CASCADE,
        related_name='images',
        verbose_name='Kamar',
        help_text='Kamar yang memiliki gambar ini.',
    )
    image = models.ImageField(
        upload_to='rooms/%Y/%m/%d/',
        verbose_name='Gambar Kamar',
        help_text='File gambar yang menampilkan kondisi aktual kamar.',
    )
    caption = models.CharField(
        max_length=255,
        blank=True,
        verbose_name='Keterangan Gambar',
        help_text='Keterangan singkat untuk membantu admin, owner, atau tenant memahami isi gambar.',
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Dibuat Pada',
        help_text='Waktu saat gambar kamar pertama kali diunggah.',
    )

    class Meta:
        ordering = ['created_at']
        verbose_name = 'Gambar Kamar'
        verbose_name_plural = 'Galeri Gambar Kamar'

    def __str__(self):
        """
        Mengembalikan label gambar kamar untuk kebutuhan admin dan debugging.

        Returns:
            str: Nomor kamar beserta identitas ringkas gambar.
        """
        if self.caption:
            return f"Kamar {self.room.room_number} - {self.caption}"
        return f"Kamar {self.room.room_number} - Gambar #{self.pk}"


class PaymentMethod(models.Model):
    """
    Menyimpan data metode pembayaran yang disediakan oleh owner kost.

    Setiap instance mewakili satu opsi pembayaran (misalnya, QRIS atau
    nomor rekening) yang dapat digunakan oleh tenant sebelum mengunggah
    bukti transfer.
    """
    kost = models.ForeignKey(
        Kost,
        on_delete=models.CASCADE,
        related_name='payment_methods',
        verbose_name='Kost',
        help_text='Kost yang menyediakan metode pembayaran ini.',
    )
    name = models.CharField(
        max_length=100,
        verbose_name='Nama Metode Pembayaran',
        help_text='Contoh: QRIS, Transfer Bank ABC',
    )
    image = models.ImageField(
        upload_to='payment_methods/%Y/%m/%d/',
        verbose_name='Gambar QRIS/Metode Pembayaran',
        help_text='Unggah gambar QRIS atau detail rekening.',
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Dibuat Pada',
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='Diperbarui Pada',
    )

    class Meta:
        ordering = ['created_at']
        unique_together = ('kost', 'name')
        verbose_name = 'Metode Pembayaran'
        verbose_name_plural = 'Daftar Metode Pembayaran'

    def __str__(self):
        """
        Mengembalikan label metode pembayaran yang mudah dikenali.

        Label ini membantu admin dan owner membaca hubungan antara kost
        dan metode pembayaran dengan cepat.

        Returns:
            str: Nama kost beserta nama metode pembayaran.
        """
        return f"{self.kost.name} - {self.name}"