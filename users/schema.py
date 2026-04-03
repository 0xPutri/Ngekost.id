from rest_framework import serializers


class AuthTokenResponseSerializer(serializers.Serializer):
    refresh = serializers.CharField(help_text='Refresh token JWT untuk memperoleh access token baru.')
    access = serializers.CharField(help_text='Access token JWT yang digunakan pada header Authorization.')


class RegisterSuccessDataSerializer(serializers.Serializer):
    username = serializers.CharField()
    email = serializers.EmailField()
    role = serializers.CharField()


class RegisterSuccessResponseSerializer(serializers.Serializer):
    pesan = serializers.CharField()
    data = RegisterSuccessDataSerializer()


class MessageOnlySerializer(serializers.Serializer):
    pesan = serializers.CharField()


class GenericStatusSerializer(serializers.Serializer):
    pesan = serializers.CharField()
    status_baru = serializers.CharField()


class PaymentUploadResponseSerializer(serializers.Serializer):
    pesan = serializers.CharField()
    data = serializers.DictField()


class VerifyPaymentRequestSerializer(serializers.Serializer):
    action = serializers.ChoiceField(
        choices=['approve', 'reject'],
        help_text='Aksi verifikasi pembayaran oleh owner. Gunakan `approve` untuk menerima atau `reject` untuk menolak.',
    )