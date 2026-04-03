import logging
from rest_framework import viewsets, mixins, filters
from django.contrib.auth import get_user_model
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import OpenApiParameter, extend_schema, extend_schema_view
from .permissions import IsAdminRole
from users.serializers import UserProfileSerializer
from kosts.models import Kost
from kosts.serializers import KostSerializer
from transactions.models import Booking
from transactions.serializers import BookingSerializer

User = get_user_model()
logger = logging.getLogger('ngekost.admin')

@extend_schema_view(
    list=extend_schema(
        tags=['Admin Panel'],
        summary='Daftar pengguna',
        description='Menampilkan daftar seluruh pengguna untuk kebutuhan pengawasan administrator.',
        parameters=[
            OpenApiParameter(name='role', description='Filter berdasarkan peran pengguna.', required=False, type=str),
            OpenApiParameter(name='is_active', description='Filter status aktif pengguna.', required=False, type=bool),
            OpenApiParameter(name='search', description='Pencarian username, email, atau nama depan.', required=False, type=str),
            OpenApiParameter(name='page', description='Nomor halaman hasil paginasi.', required=False, type=int),
        ],
    ),
    retrieve=extend_schema(
        tags=['Admin Panel'],
        summary='Detail pengguna',
        description='Mengambil detail satu pengguna untuk kebutuhan administratif.',
    ),
    destroy=extend_schema(
        tags=['Admin Panel'],
        summary='Hapus pengguna',
        description='Menghapus akun pengguna dari sistem. Khusus administrator.',
    ),
)
class AdminUserViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, mixins.DestroyModelMixin, viewsets.GenericViewSet):
    """
    Mengelola data pengguna pada panel admin API.

    ViewSet ini memberi administrator akses untuk melihat detail, mencari,
    dan menghapus akun pengguna sesuai kebutuhan pengawasan sistem.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserProfileSerializer
    permission_classes = [IsAdminRole]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]

    filterset_fields = ['role', 'is_active']
    search_fields = ['username', 'email', 'first_name']

    def perform_destroy(self, instance):
        """
        Menghapus akun pengguna dan mencatat aktivitas admin.

        Args:
            instance (CustomUser): Pengguna yang akan dihapus.
        """
        logger.warning(
            'Administrator menghapus akun pengguna.',
            extra={'user_id_target': instance.id, 'role_target': instance.role, 'email': instance.email},
        )
        instance.delete()

class AdminKostViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, mixins.DestroyModelMixin, viewsets.GenericViewSet):
    """
    Mengelola data kost pada panel admin API.

    ViewSet ini dipakai administrator untuk meninjau, menelusuri, dan
    menghapus data kost yang ada di platform.
    """
    queryset = Kost.objects.select_related('owner').prefetch_related('rooms').order_by('-created_at')
    serializer_class = KostSerializer
    permission_classes = [IsAdminRole]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]

    filterset_fields = ['owner__username']
    search_fields = ['name', 'address']

    def perform_destroy(self, instance):
        """
        Menghapus data kost dan mencatat aktivitas admin.

        Args:
            instance (Kost): Kost yang akan dihapus.
        """
        logger.warning(
            'Administrator menghapus data kost.',
            extra={'kost_id': instance.id, 'owner_id': instance.owner_id, 'nama_kost': instance.name},
        )
        instance.delete()

class AdminBookingViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    """
    Menyajikan data booking untuk kebutuhan audit administrator.

    ViewSet ini membantu admin memantau transaksi tenant dan owner tanpa
    memberikan operasi perubahan status secara langsung.
    """
    queryset = Booking.objects.select_related(
        'tenant', 'room', 'room__kost'
    ).prefetch_related('payment_proof').order_by('-created_at')
    serializer_class = BookingSerializer
    permission_classes = [IsAdminRole]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]

    filterset_fields = ['status']
    search_fields = ['tenant__username', 'room__kost__name', 'room__room_number']


AdminKostViewSet = extend_schema_view(
    list=extend_schema(
        tags=['Admin Panel'],
        summary='Daftar kost untuk admin',
        description='Menampilkan seluruh data kost untuk kebutuhan audit dan moderasi administrator.',
        parameters=[
            OpenApiParameter(name='owner__username', description='Filter berdasarkan username owner.', required=False, type=str),
            OpenApiParameter(name='search', description='Pencarian nama atau alamat kost.', required=False, type=str),
            OpenApiParameter(name='page', description='Nomor halaman hasil paginasi.', required=False, type=int),
        ],
    ),
    retrieve=extend_schema(
        tags=['Admin Panel'],
        summary='Detail kost untuk admin',
        description='Mengambil detail kost tertentu pada panel administrator.',
    ),
    destroy=extend_schema(
        tags=['Admin Panel'],
        summary='Hapus kost oleh admin',
        description='Menghapus data kost dari sistem. Khusus administrator.',
    ),
)(AdminKostViewSet)


AdminBookingViewSet = extend_schema_view(
    list=extend_schema(
        tags=['Admin Panel'],
        summary='Daftar booking untuk admin',
        description='Menampilkan seluruh transaksi booking untuk pengawasan operasional administrator.',
        parameters=[
            OpenApiParameter(name='status', description='Filter berdasarkan status booking.', required=False, type=str),
            OpenApiParameter(
                name='search',
                description='Pencarian berdasarkan username tenant, nama kost, atau nomor kamar.',
                required=False,
                type=str,
            ),
            OpenApiParameter(name='page', description='Nomor halaman hasil paginasi.', required=False, type=int),
        ],
    ),
    retrieve=extend_schema(
        tags=['Admin Panel'],
        summary='Detail booking untuk admin',
        description='Mengambil detail transaksi booking tertentu untuk kebutuhan audit administrator.',
    ),
)(AdminBookingViewSet)