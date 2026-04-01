import logging
from rest_framework import viewsets, filters
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from django_filters.rest_framework import DjangoFilterBackend
from .models import Kost, Room
from .serializers import KostSerializer, KostDetailSerializer, RoomSerializer
from .permissions import IsOwnerOrReadOnly

logger = logging.getLogger('ngekost.kosts')

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