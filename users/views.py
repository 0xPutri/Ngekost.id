import logging
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView
from drf_spectacular.utils import OpenApiExample, OpenApiResponse, extend_schema, extend_schema_view
from django.contrib.auth import get_user_model
from .serializers import RegisterSerializer, UserProfileSerializer, CustomTokenObtainPairSerializer
from .schema import AuthTokenResponseSerializer, RegisterSuccessResponseSerializer

User = get_user_model()
logger = logging.getLogger('ngekost.users')

@extend_schema(
    tags=['Autentikasi'],
    summary='Login pengguna',
    description=(
        'Mengautentikasi pengguna menggunakan `username` dan `password`, lalu '
        'mengembalikan pasangan token JWT berupa `access` dan `refresh`.'
    ),
    responses={
        200: AuthTokenResponseSerializer,
        401: OpenApiResponse(description='Kredensial tidak valid.'),
    },
    examples=[
        OpenApiExample(
            'Contoh Login',
            value={'username': 'tenant_demo', 'password': 'KatasandiAman123!'},
            request_only=True,
        ),
        OpenApiExample(
            'Contoh Response Login',
            value={'refresh': '<refresh_token>', 'access': '<access_token>'},
            response_only=True,
            status_codes=['200'],
        ),
    ],
)
class CustomTokenObtainPairView(TokenObtainPairView):
    """
    Menangani proses login dan penerbitan token JWT pengguna.

    View ini juga mencatat hasil autentikasi agar aktivitas login dapat
    dipantau untuk kebutuhan operasional dan audit dasar.
    """
    serializer_class = CustomTokenObtainPairSerializer

    def post(self, request, *args, **kwargs):
        """
        Memproses permintaan login pengguna.

        Args:
            request (Request): Request yang memuat username dan password.

        Returns:
            Response: Respons token JWT atau pesan kegagalan autentikasi.
        """
        response = super().post(request, *args, **kwargs)
        username = request.data.get('username')

        if response.status_code == status.HTTP_200_OK:
            logger.info(
                'Autentikasi pengguna berhasil.',
                extra={'username': username, 'status_code': response.status_code},
            )
        else:
            logger.warning(
                'Autentikasi pengguna gagal.',
                extra={'username': username, 'status_code': response.status_code},
            )

        return response

@extend_schema(
    tags=['Autentikasi'],
    summary='Registrasi akun tenant',
    description=(
        'Mendaftarkan akun baru untuk peran `tenant`. Registrasi publik tidak '
        'dapat digunakan untuk membuat akun `owner` atau `admin`.'
    ),
    responses={
        201: RegisterSuccessResponseSerializer,
        400: OpenApiResponse(description='Validasi data gagal, misalnya password tidak cocok atau role tidak valid.'),
    },
)
class RegisterView(generics.CreateAPIView):
    """
    Menangani registrasi akun tenant baru pada platform.

    Endpoint ini dibuka untuk publik, tetapi tetap membatasi pembuatan akun
    hanya pada peran tenant sesuai aturan bisnis aplikasi.
    """
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer

    def create(self, request, *args, **kwargs):
        """
        Memvalidasi data registrasi dan mengembalikan respons yang ramah klien.

        Args:
            request (Request): Request yang memuat data akun baru.

        Returns:
            Response: Respons sukses registrasi beserta data ringkas akun.
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = self.perform_create(serializer)
        logger.info(
            'Registrasi akun baru berhasil diproses.',
            extra={'user_id_baru': user.id, 'role': user.role, 'email': user.email},
        )

        headers = self.get_success_headers(serializer.data)
        return Response(
            {
                "pesan": "Akun berhasil dibuat. Silakan login.",
                "data": {
                    "username": user.username,
                    "email": user.email,
                    "role": user.role
                }
            },
            status=status.HTTP_201_CREATED,
            headers=headers
        )
    
    def perform_create(self, serializer):
        """
        Menyimpan akun baru menggunakan serializer registrasi.

        Args:
            serializer (RegisterSerializer): Serializer yang sudah tervalidasi.

        Returns:
            CustomUser: Pengguna baru yang berhasil dibuat.
        """
        return serializer.save()

@extend_schema_view(
    get=extend_schema(
        tags=['Profil Pengguna'],
        summary='Lihat profil pengguna aktif',
        description='Mengambil detail profil milik pengguna yang sedang terautentikasi.',
    ),
    put=extend_schema(
        tags=['Profil Pengguna'],
        summary='Perbarui profil pengguna aktif',
        description='Memperbarui profil pengguna yang sedang login secara penuh.',
    ),
    patch=extend_schema(
        tags=['Profil Pengguna'],
        summary='Perbarui sebagian profil pengguna aktif',
        description='Memperbarui sebagian data profil pengguna yang sedang login.',
    ),
)
class UserProfileView(generics.RetrieveUpdateAPIView):
    """
    Menampilkan dan memperbarui profil pengguna yang sedang login.

    View ini memastikan setiap pengguna hanya berinteraksi dengan profilnya
    sendiri tanpa perlu mengirim identitas target secara terpisah.
    """
    serializer_class = UserProfileSerializer
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        """
        Mengambil objek pengguna aktif dari request saat ini.

        Returns:
            CustomUser: Pengguna yang sedang terautentikasi.
        """
        return self.request.user
    
    def update(self, request, *args, **kwargs):
        """
        Memperbarui data profil pengguna aktif.

        Args:
            request (Request): Request yang memuat data profil baru.

        Returns:
            Response: Respons sukses beserta data profil terbaru.
        """
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        logger.info(
            'Profil pengguna berhasil diperbarui.',
            extra={'user_id_target': instance.id, 'partial': partial},
        )

        if getattr(instance, '_prefetched_objects_cache', None):
            instance._prefetched_objects_cache = {}

        return Response({
            "pesan": "Profil berhasil diperbarui.",
            "data": serializer.data
        })