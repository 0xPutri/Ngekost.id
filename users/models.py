from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    """
    Menyimpan data pengguna yang terlibat dalam platform Ngekost.id.

    Model ini memperluas pengguna bawaan Django agar sistem dapat membedakan
    peran admin, owner, dan tenant beserta informasi kontak dasarnya.
    """
    ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('owner', 'Owner'),
        ('tenant', 'Tenant'),
    )

    role = models.CharField(
        max_length=10,
        choices=ROLE_CHOICES,
        default='tenant',
        verbose_name='Peran Pengguna',
        help_text='Tentukan peran pengguna dalam sistem: admin, owner, atau tenant.',
    )
    phone_number = models.CharField(
        max_length=15,
        blank=True,
        null=True,
        verbose_name='Nomor Telepon',
        help_text='Nomor telepon aktif yang dapat dihubungi untuk kebutuhan operasional atau verifikasi.',
    )
    email = models.EmailField(
        unique=True,
        verbose_name='Alamat Email',
        help_text='Alamat email unik yang digunakan untuk login dan komunikasi akun.',
    )

    class Meta:
        verbose_name = 'Pengguna'
        verbose_name_plural = 'Pengguna'

    def __str__(self):
        """
        Mengembalikan representasi singkat pengguna untuk tampilan internal.

        Format ini membantu admin dan developer mengenali username beserta
        peran aktif pengguna saat data ditampilkan.

        Returns:
            str: Nama pengguna beserta label perannya.
        """
        return f"{self.username} ({self.get_role_display()})"