from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password

User = get_user_model()

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    """
    Menyesuaikan payload token JWT dengan identitas pengguna.

    Serializer ini menambahkan informasi sederhana seperti username dan role
    agar klien lebih mudah membaca konteks sesi yang sedang aktif.
    """

    @classmethod
    def get_token(cls, user):
        """
        Membentuk token JWT dan menambahkan klaim penting pengguna.

        Args:
            user (CustomUser): Pengguna yang berhasil diautentikasi.

        Returns:
            Token: Token JWT dengan klaim username dan role.
        """
        token = super().get_token(user)
        token['username'] = user.username
        token['role'] = user.role
        return token
    
class UserProfileSerializer(serializers.ModelSerializer):
    """
    Menyajikan data profil pengguna yang aman untuk dibaca dan diperbarui.

    Field yang bersifat identitas inti tetap dibuat read-only agar perubahan
    profil tidak merusak struktur akun di sistem.
    """
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'first_name', 'last_name', 'phone_number', 'role')
        read_only_fields = ('id', 'username', 'role')

class RegisterSerializer(serializers.ModelSerializer):
    """
    Memvalidasi dan membuat akun tenant melalui registrasi publik.

    Serializer ini memastikan hanya peran tenant yang dapat dibuat dari
    endpoint publik serta memeriksa kecocokan password sebelum akun disimpan.
    """
    PUBLIC_REGISTRATION_ROLE = 'tenant'

    password = serializers.CharField(
        write_only=True, required=True, validators=[validate_password], style={'input_type': 'password'}
    )
    password_confirm = serializers.CharField(
        write_only=True, required=True, style={'input_type': 'password'}
    )

    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'password_confirm', 'first_name', 'last_name', 'phone_number', 'role')

    def validate(self, attrs):
        """
        Memeriksa konsistensi data registrasi sebelum akun dibuat.

        Args:
            attrs (dict): Data mentah registrasi yang dikirim klien.

        Returns:
            dict: Data registrasi yang sudah lolos validasi.

        Raises:
            ValidationError: Jika password tidak cocok atau role tidak diizinkan.
        """
        if attrs['password'] != attrs['password_confirm']:
            raise serializers.ValidationError({"Password": "Password dan Konfirmasi Password tidak cocok."})

        requested_role = attrs.get('role', self.PUBLIC_REGISTRATION_ROLE)
        if requested_role != self.PUBLIC_REGISTRATION_ROLE:
            raise serializers.ValidationError({
                "role": "Registrasi publik hanya dapat membuat akun tenant."
            })

        return attrs
    
    def create(self, validated_data):
        """
        Membuat akun tenant baru dari data yang telah tervalidasi.

        Args:
            validated_data (dict): Data registrasi yang siap disimpan.

        Returns:
            CustomUser: Objek pengguna baru dengan peran tenant.
        """
        validated_data.pop('password_confirm')
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', ''),
            phone_number=validated_data.get('phone_number', ''),
            role=self.PUBLIC_REGISTRATION_ROLE
        )
        return user