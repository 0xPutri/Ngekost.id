from rest_framework import serializers


class AuthTokenResponseSerializer(serializers.Serializer):
    """
    Mendeskripsikan payload token JWT pada dokumentasi API.

    Serializer ini dipakai untuk menjelaskan bentuk respons login pada
    schema OpenAPI tanpa memengaruhi proses autentikasi.
    """
    refresh = serializers.CharField(help_text='Refresh token JWT untuk memperoleh access token baru.')
    access = serializers.CharField(help_text='Access token JWT yang digunakan pada header Authorization.')


class RegisterSuccessDataSerializer(serializers.Serializer):
    """
    Menjelaskan data inti akun yang dikembalikan setelah registrasi.

    Struktur ini membantu dokumentasi API tetap konsisten dan mudah dibaca
    oleh pengembang frontend.
    """
    username = serializers.CharField()
    email = serializers.EmailField()
    role = serializers.CharField()


class RegisterSuccessResponseSerializer(serializers.Serializer):
    """
    Menjelaskan format respons sukses saat akun tenant berhasil dibuat.

    Serializer schema ini memisahkan pesan umum dan data akun ringkas agar
    dokumentasi endpoint registrasi tetap jelas.
    """
    pesan = serializers.CharField()
    data = RegisterSuccessDataSerializer()


class MessageOnlySerializer(serializers.Serializer):
    """
    Menjelaskan respons sederhana yang hanya memuat pesan.

    Serializer ini berguna untuk endpoint yang tidak perlu mengirim data
    tambahan selain informasi hasil proses.
    """
    pesan = serializers.CharField()


class GenericStatusSerializer(serializers.Serializer):
    """
    Menjelaskan respons status generik pada proses bisnis tertentu.

    Biasanya dipakai saat sistem mengembalikan pesan hasil aksi dan status
    terbaru dari entitas yang diproses.
    """
    pesan = serializers.CharField()
    status_baru = serializers.CharField()


class PaymentUploadResponseSerializer(serializers.Serializer):
    """
    Menjelaskan respons unggah bukti pembayaran pada dokumentasi API.

    Struktur ini menampilkan pesan hasil unggahan dan data file yang telah
    diterima oleh sistem.
    """
    pesan = serializers.CharField()
    data = serializers.DictField()


class VerifyPaymentRequestSerializer(serializers.Serializer):
    """
    Menjelaskan payload aksi verifikasi pembayaran oleh owner.

    Serializer schema ini membantu dokumentasi menjelaskan nilai aksi yang
    diperbolehkan saat owner memproses bukti pembayaran.
    """
    action = serializers.ChoiceField(
        choices=['approve', 'reject'],
        help_text='Aksi verifikasi pembayaran oleh owner. Gunakan `approve` untuk menerima atau `reject` untuk menolak.',
    )