from rest_framework import viewsets, filters
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from django_filters.rest_framework import DjangoFilterBackend
from .models import Kost, Room
from .serializers import KostSerializer, KostDetailSerializer, RoomSerializer
from .permissions import IsOwnerOrReadOnly

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
        serializer.save(owner=self.request.user)

class RoomViewSet(viewsets.ModelViewSet):
    queryset = Room.objects.all().select_related('kost') # Mencegah N+1 Queries
    serializer_class = RoomSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]

    filterset_fields = ['kost', 'status']
    ordering_fields = ['price']