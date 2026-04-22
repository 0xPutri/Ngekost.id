import logging
from rest_framework import viewsets, filters, parsers
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import OpenApiParameter, OpenApiResponse, extend_schema, extend_schema_view
from .models import Kost, KostImage, PaymentMethod, Room, RoomImage
from .serializers import (
    KostDetailSerializer,
    KostImageSerializer,
    KostImageWriteSerializer,
    KostSerializer,
    PaymentMethodSerializer,
    RoomImageSerializer,
    RoomImageWriteSerializer,
    RoomSerializer,
)
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
        exclude=True,
    ),
    update=extend_schema(
        tags=['Kost'],
        summary='Perbarui kost',
        description='Memperbarui seluruh data kost milik owner yang sedang login.',
        exclude=True,
    ),
    partial_update=extend_schema(
        tags=['Kost'],
        summary='Perbarui sebagian data kost',
        description='Memperbarui sebagian atribut kost milik owner yang sedang login.',
        exclude=True,
    ),
    destroy=extend_schema(
        tags=['Kost'],
        summary='Hapus kost',
        description='Menghapus data kost milik owner yang sedang login.',
        responses={204: OpenApiResponse(description='Kost berhasil dihapus.')},
        exclude=True,
    ),
)
class KostViewSet(viewsets.ModelViewSet):
    """
    Mengelola endpoint daftar, detail, dan pemeliharaan data kost.

    ViewSet ini melayani kebutuhan tenant untuk mencari kost sekaligus
    kebutuhan owner untuk membuat dan mengelola properti miliknya.
    """
    queryset = Kost.objects.all().prefetch_related('images', 'rooms__images', 'rooms') # Mencegah N+1 Queries
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]

    filterset_fields = ['address']
    search_fields = ['name', 'address', 'facilities']
    ordering_fields = ['created_at']

    def get_serializer_class(self):
        """
        Memilih serializer sesuai jenis aksi yang sedang dijalankan.

        Returns:
            type[Serializer]: Serializer detail untuk `retrieve`, selain itu serializer ringkas.
        """
        if self.action == 'retrieve':
            return KostDetailSerializer
        return KostSerializer
    
    def perform_create(self, serializer):
        """
        Menyimpan kost baru dengan owner dari pengguna aktif.

        Args:
            serializer (KostSerializer): Serializer yang sudah tervalidasi.
        """
        kost = serializer.save(owner=self.request.user)
        logger.info(
            'Data kost baru berhasil dibuat.',
            extra={'kost_id': kost.id, 'owner_id': self.request.user.id, 'nama_kost': kost.name},
        )

    def perform_update(self, serializer):
        """
        Menyimpan perubahan data kost dan mencatat aktivitasnya.

        Args:
            serializer (KostSerializer): Serializer yang membawa data terbaru.
        """
        kost = serializer.save()
        logger.info(
            'Data kost berhasil diperbarui.',
            extra={'kost_id': kost.id, 'owner_id': kost.owner_id, 'nama_kost': kost.name},
        )

    def perform_destroy(self, instance):
        """
        Menghapus data kost yang dipilih pengguna berwenang.

        Args:
            instance (Kost): Objek kost yang akan dihapus.
        """
        logger.warning(
            'Data kost akan dihapus.',
            extra={'kost_id': instance.id, 'owner_id': instance.owner_id, 'nama_kost': instance.name},
        )
        instance.delete()

class RoomViewSet(viewsets.ModelViewSet):
    """
    Mengelola endpoint kamar pada setiap properti kost.

    ViewSet ini dipakai owner untuk menambah dan memperbarui kamar, serta
    dipakai tenant untuk melihat ketersediaan kamar secara terbuka.
    """
    queryset = Room.objects.all().select_related('kost').prefetch_related('images') # Mencegah N+1 Queries
    serializer_class = RoomSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]

    filterset_fields = ['kost', 'status']
    ordering_fields = ['price']

    def perform_create(self, serializer):
        """
        Menyimpan kamar baru dan mencatat aktivitas pembuatannya.

        Args:
            serializer (RoomSerializer): Serializer yang sudah tervalidasi.
        """
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
        """
        Menyimpan perubahan data kamar dan mencatat hasilnya.

        Args:
            serializer (RoomSerializer): Serializer yang membawa data terbaru.
        """
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
        """
        Menghapus data kamar yang dipilih pengguna berwenang.

        Args:
            instance (Room): Objek kamar yang akan dihapus.
        """
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


@extend_schema_view(
    list=extend_schema(
        tags=['Kost'],
        summary='Daftar gambar kost',
        description='Mengambil daftar gambar kost. Publik dapat membaca, owner dapat mengelola gambar miliknya.',
        parameters=[
            OpenApiParameter(name='kost', description='ID kost untuk memfilter gambar.', required=False, type=int),
            OpenApiParameter(name='page', description='Nomor halaman hasil paginasi.', required=False, type=int),
        ],
    ),
    retrieve=extend_schema(
        tags=['Kost'],
        summary='Detail gambar kost',
        description='Mengambil detail satu gambar kost.',
    ),
    create=extend_schema(
        tags=['Kost'],
        summary='Unggah gambar kost',
        description='Mengunggah satu gambar ke kost milik owner yang sedang login.',
        request=KostImageWriteSerializer,
        exclude=True,
    ),
    update=extend_schema(
        tags=['Kost'],
        summary='Perbarui gambar kost',
        description='Memperbarui data gambar kost milik owner yang sedang login.',
        exclude=True,
    ),
    partial_update=extend_schema(
        tags=['Kost'],
        summary='Perbarui sebagian gambar kost',
        description='Memperbarui sebagian data gambar kost milik owner yang sedang login.',
        exclude=True,
    ),
    destroy=extend_schema(
        tags=['Kost'],
        summary='Hapus gambar kost',
        description='Menghapus gambar kost milik owner yang sedang login.',
        responses={204: OpenApiResponse(description='Gambar kost berhasil dihapus.')},
        exclude=True,
    ),
)
class KostImageViewSet(viewsets.ModelViewSet):
    """
    Mengelola endpoint galeri gambar untuk properti kost.

    ViewSet ini memungkinkan owner menambah, memperbarui, dan menghapus
    gambar kost, sementara publik tetap dapat melihat galeri yang tersedia.
    """

    queryset = KostImage.objects.all().select_related('kost', 'kost__owner')
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    parser_classes = [parsers.MultiPartParser, parsers.FormParser, parsers.JSONParser]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['kost']

    def get_serializer_class(self):
        if self.action in ('create', 'update', 'partial_update'):
            return KostImageWriteSerializer
        return KostImageSerializer


@extend_schema_view(
    list=extend_schema(
        tags=['Kamar'],
        summary='Daftar gambar kamar',
        description='Mengambil daftar gambar kamar. Publik dapat membaca, owner dapat mengelola gambar miliknya.',
        parameters=[
            OpenApiParameter(name='room', description='ID kamar untuk memfilter gambar.', required=False, type=int),
            OpenApiParameter(name='page', description='Nomor halaman hasil paginasi.', required=False, type=int),
        ],
    ),
    retrieve=extend_schema(
        tags=['Kamar'],
        summary='Detail gambar kamar',
        description='Mengambil detail satu gambar kamar.',
    ),
    create=extend_schema(
        tags=['Kamar'],
        summary='Unggah gambar kamar',
        description='Mengunggah satu gambar ke kamar pada kost milik owner yang sedang login.',
        request=RoomImageWriteSerializer,
        exclude=True,
    ),
    update=extend_schema(
        tags=['Kamar'],
        summary='Perbarui gambar kamar',
        description='Memperbarui data gambar kamar milik owner yang sedang login.',
        exclude=True,
    ),
    partial_update=extend_schema(
        tags=['Kamar'],
        summary='Perbarui sebagian gambar kamar',
        description='Memperbarui sebagian data gambar kamar milik owner yang sedang login.',
        exclude=True,
    ),
    destroy=extend_schema(
        tags=['Kamar'],
        summary='Hapus gambar kamar',
        description='Menghapus gambar kamar milik owner yang sedang login.',
        responses={204: OpenApiResponse(description='Gambar kamar berhasil dihapus.')},
        exclude=True,
    ),
)
class RoomImageViewSet(viewsets.ModelViewSet):
    """
    Mengelola endpoint galeri gambar untuk setiap kamar.

    ViewSet ini memungkinkan owner mengelola dokumentasi visual kamar tanpa
    mencampur operasi upload file ke endpoint kamar utama.
    """

    queryset = RoomImage.objects.all().select_related('room', 'room__kost', 'room__kost__owner')
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    parser_classes = [parsers.MultiPartParser, parsers.FormParser, parsers.JSONParser]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['room']

    def get_serializer_class(self):
        if self.action in ('create', 'update', 'partial_update'):
            return RoomImageWriteSerializer
        return RoomImageSerializer


@extend_schema_view(
    list=extend_schema(
        tags=['Metode Pembayaran'],
        summary='Daftar metode pembayaran kost',
        description='Mengambil daftar metode pembayaran yang tersedia untuk sebuah kost.',
    ),
    retrieve=extend_schema(
        tags=['Metode Pembayaran'],
        summary='Detail metode pembayaran kost',
        description='Mengambil detail satu metode pembayaran yang tersedia untuk sebuah kost.',
    ),
    create=extend_schema(
        tags=['Metode Pembayaran'],
        summary='Unggah metode pembayaran baru',
        description='Menambahkan metode pembayaran baru ke sebuah kost. Hanya dapat dilakukan oleh pemilik kost tersebut.',
        exclude=True,
    ),
    destroy=extend_schema(
        tags=['Metode Pembayaran'],
        summary='Hapus metode pembayaran',
        description='Menghapus metode pembayaran dari sebuah kost. Hanya dapat dilakukan oleh pemilik kost tersebut.',
        exclude=True,
    )
)
class PaymentMethodViewSet(viewsets.ModelViewSet):
    """
    Mengelola metode pembayaran untuk setiap kost.

    Endpoint ini membantu tenant melihat opsi pembayaran yang tersedia dan
    membantu owner mengelola metode pembayaran miliknya.
    """
    serializer_class = PaymentMethodSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    parser_classes = [parsers.MultiPartParser, parsers.FormParser, parsers.JSONParser]
    http_method_names = ['get', 'post', 'delete', 'head', 'options']

    def get_queryset(self):
        """
        Mengambil daftar metode pembayaran milik kost yang diminta.

        Fungsi ini membaca `kost_pk` dari URL agar data yang tampil tetap
        sesuai dengan kost yang sedang dibuka.

        Returns:
            QuerySet: Daftar metode pembayaran untuk kost terkait.
        """
        kost_pk = self.kwargs.get('kost_pk')
        if kost_pk:
            return PaymentMethod.objects.filter(kost_id=kost_pk)
        return PaymentMethod.objects.none()

    def perform_create(self, serializer):
        """
        Menyimpan metode pembayaran baru untuk kost yang dipilih.

        Fungsi ini memastikan hanya owner dari kost terkait yang dapat
        menambahkan metode pembayaran baru.

        Args:
            serializer (PaymentMethodSerializer): Serializer yang sudah valid.

        Raises:
            PermissionDenied: Jika kost tidak ditemukan atau bukan milik owner.
        """
        from rest_framework.exceptions import PermissionDenied, ValidationError
        
        kost_pk = self.kwargs.get('kost_pk')
        try:
            kost = Kost.objects.get(pk=kost_pk)
        except Kost.DoesNotExist:
            raise PermissionDenied('Kost tidak ditemukan.')

        if kost.owner != self.request.user:
            raise PermissionDenied('Anda bukan pemilik kost ini.')
            
        name = serializer.validated_data.get('name')
        if PaymentMethod.objects.filter(kost=kost, name__iexact=name).exists():
            raise ValidationError({'name': f'Metode pembayaran "{name}" sudah ada untuk kost ini.'})

        serializer.save(kost=kost)

    def perform_destroy(self, instance):
        """
        Menghapus metode pembayaran milik kost yang sesuai.

        Fungsi ini menjaga agar hanya owner yang berwenang yang dapat
        menghapus metode pembayaran tersebut.

        Args:
            instance (PaymentMethod): Objek metode pembayaran yang dihapus.

        Raises:
            PermissionDenied: Jika pengguna bukan pemilik metode pembayaran.
        """
        from rest_framework.exceptions import PermissionDenied

        if instance.kost.owner != self.request.user:
            raise PermissionDenied('Anda tidak diizinkan menghapus metode pembayaran ini.')
        
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
        exclude=True,
    ),
    update=extend_schema(
        tags=['Kamar'],
        summary='Perbarui kamar',
        description='Memperbarui seluruh data kamar pada kost milik owner yang sedang login.',
        exclude=True,
    ),
    partial_update=extend_schema(
        tags=['Kamar'],
        summary='Perbarui sebagian data kamar',
        description='Memperbarui sebagian atribut kamar pada kost milik owner yang sedang login.',
        exclude=True,
    ),
    destroy=extend_schema(
        tags=['Kamar'],
        summary='Hapus kamar',
        description='Menghapus kamar dari kost milik owner yang sedang login.',
        responses={204: OpenApiResponse(description='Kamar berhasil dihapus.')},
        exclude=True,
    ),
)(RoomViewSet)