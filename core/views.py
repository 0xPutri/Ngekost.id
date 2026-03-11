from rest_framework import viewsets, mixins, filters
from django.contrib.auth import get_user_model
from django_filters.rest_framework import DjangoFilterBackend
from .permissions import IsAdminRole
from users.serializers import UserProfileSerializer
from kosts.models import Kost
from kosts.serializers import KostSerializer
from transactions.models import Booking
from transactions.serializers import BookingSerializer

User = get_user_model()

class AdminUserViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, mixins.DestroyModelMixin, viewsets.GenericViewSet):
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserProfileSerializer
    permission_classes = [IsAdminRole]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]

    filterset_fields = ['role', 'is_active']
    search_fields = ['username', 'email', 'first_name']

class AdminKostViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, mixins.DestroyModelMixin, viewsets.GenericViewSet):
    queryset = Kost.objects.select_related('owner').prefetch_related('rooms').order_by('-created_at')
    serializer_class = KostSerializer
    permission_classes = [IsAdminRole]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]

    filterset_fields = ['owner__username']
    search_fields = ['name', 'address']

class AdminBookingViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    queryset = Booking.objects.select_related(
        'tenant', 'room', 'room__kost'
    ).prefetch_related('payment_proof').order_by('-created_at')
    serializer_class = BookingSerializer
    permission_classes = [IsAdminRole]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]

    filterset_fields = ['status']
    search_fields = ['tenant__username', 'room__kost__name', 'room__room_number']