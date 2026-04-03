import logging
from rest_framework import viewsets, filters
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import OpenApiParameter, OpenApiResponse, extend_schema, extend_schema_view
from .models import Kost, Room
from .serializers import KostSerializer, KostDetailSerializer, RoomSerializer
from .permissions import IsOwnerOrReadOnly

logger = logging.getLogger('ngekost.kosts')

@extend_schema_view(
    list=extend_schema(
        tags=['Kost'],
        summary='Daftar kost',
        description='Mengambil daftar kost yang tersedia di platform. Mendukung filter, pencarian, dan pengurutan.',
        parameters=[
            OpenApiParameter(name='address', description='Filter berdasarkan alamat kost.', required=False, type=str),
            OpenApiParameter(name='search', description='Pencarian pada nama kost, alamat, atau fasilitas.', required=False, type=str),
            OpenApiParameter(name='ordering', description='Urutkan berdasarkan `created_at`.', required=False, type=str),
            OpenApiParameter(name='page', description='Nomor halaman hasil paginasi.', required=False, type=int),
        ],
    ),
    retrieve=extend_schema(
        tags=['Kost'],
        summary='Detail kost',
        description='Mengambil detail satu kost beserta daftar kamar yang terkait.',
    ),
    create=extend_schema(
        tags=['Kost'],
        summary='Buat kost baru',
        description='Mendaftarkan data kost baru. Hanya dapat dilakukan oleh pengguna dengan peran owner.',
        responses={201: KostSerializer, 403: OpenApiResponse(description='Hanya owner yang dapat membuat kost.')},
    ),
    update=extend_schema(
        tags=['Kost'],
        summary='Perbarui kost',
        description='Memperbarui seluruh data kost milik owner yang sedang login.',
    ),
    partial_update=extend_schema(
        tags=['Kost'],
        summary='Perbarui sebagian data kost',
        description='Memperbarui sebagian atribut kost milik owner yang sedang login.',
    ),
    destroy=extend_schema(
        tags=['Kost'],
        summary='Hapus kost',
        description='Menghapus data kost milik owner yang sedang login.',
        responses={204: OpenApiResponse(description='Kost berhasil dihapus.')},
    ),
)
class KostViewSet(viewsets.ModelViewSet):
    queryset = Kost.objects.all().prefetch_related('rooms') # Mencegah N+1 Queries
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]

    filterset_fields = ['address']
    search_fields = ['name', 'address', 'facilities']
    ordering_fields = ['created_at']

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return KostDetailSerializer
        return KostSerializer
    
    def perform_create(self, serializer):
        kost = serializer.save(owner=self.request.user)
        logger.info(
            'Data kost baru berhasil dibuat.',
            extra={'kost_id': kost.id, 'owner_id': self.request.user.id, 'nama_kost': kost.name},
        )

    def perform_update(self, serializer):
        kost = serializer.save()
        logger.info(
            'Data kost berhasil diperbarui.',
            extra={'kost_id': kost.id, 'owner_id': kost.owner_id, 'nama_kost': kost.name},
        )

    def perform_destroy(self, instance):
        logger.warning(
            'Data kost akan dihapus.',
            extra={'kost_id': instance.id, 'owner_id': instance.owner_id, 'nama_kost': instance.name},
        )
        instance.delete()

class RoomViewSet(viewsets.ModelViewSet):
    queryset = Room.objects.all().select_related('kost') # Mencegah N+1 Queries
    serializer_class = RoomSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]

    filterset_fields = ['kost', 'status']
    ordering_fields = ['price']

    def perform_create(self, serializer):
        room = serializer.save()
        logger.info(
            'Data kamar baru berhasil dibuat.',
            extra={
                'room_id': room.id,
                'kost_id': room.kost_id,
                'nomor_kamar': room.room_number,
                'status_kamar': room.status,
            },
        )

    def perform_update(self, serializer):
        room = serializer.save()
        logger.info(
            'Data kamar berhasil diperbarui.',
            extra={
                'room_id': room.id,
                'kost_id': room.kost_id,
                'nomor_kamar': room.room_number,
                'status_kamar': room.status,
            },
        )

    def perform_destroy(self, instance):
        logger.warning(
            'Data kamar akan dihapus.',
            extra={
                'room_id': instance.id,
                'kost_id': instance.kost_id,
                'nomor_kamar': instance.room_number,
                'status_kamar': instance.status,
            },
        )
        instance.delete()


RoomViewSet = extend_schema_view(
    list=extend_schema(
        tags=['Kamar'],
        summary='Daftar kamar',
        description='Mengambil daftar kamar. Mendukung filter berdasarkan kost dan status, serta pengurutan harga.',
        parameters=[
            OpenApiParameter(name='kost', description='ID kost untuk memfilter kamar.', required=False, type=int),
            OpenApiParameter(
                name='status',
                description='Filter status kamar: `available`, `booked`, atau `occupied`.',
                required=False,
                type=str,
            ),
            OpenApiParameter(name='ordering', description='Urutkan berdasarkan `price`.', required=False, type=str),
            OpenApiParameter(name='page', description='Nomor halaman hasil paginasi.', required=False, type=int),
        ],
    ),
    retrieve=extend_schema(
        tags=['Kamar'],
        summary='Detail kamar',
        description='Mengambil detail satu kamar.',
    ),
    create=extend_schema(
        tags=['Kamar'],
        summary='Buat kamar baru',
        description='Menambahkan kamar baru pada kost milik owner yang sedang login.',
    ),
    update=extend_schema(
        tags=['Kamar'],
        summary='Perbarui kamar',
        description='Memperbarui seluruh data kamar pada kost milik owner yang sedang login.',
    ),
    partial_update=extend_schema(
        tags=['Kamar'],
        summary='Perbarui sebagian data kamar',
        description='Memperbarui sebagian atribut kamar pada kost milik owner yang sedang login.',
    ),
    destroy=extend_schema(
        tags=['Kamar'],
        summary='Hapus kamar',
        description='Menghapus kamar dari kost milik owner yang sedang login.',
        responses={204: OpenApiResponse(description='Kamar berhasil dihapus.')},
    ),
)(RoomViewSet)