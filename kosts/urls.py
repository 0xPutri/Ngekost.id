from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import KostImageViewSet, KostViewSet, PaymentMethodViewSet, RoomImageViewSet, RoomViewSet

app_name = 'kosts'

router = DefaultRouter()
router.register(r'kosts', KostViewSet, basename='kost')
router.register(r'rooms', RoomViewSet, basename='room')
router.register(r'kost-images', KostImageViewSet, basename='kost-image')
router.register(r'room-images', RoomImageViewSet, basename='room-image')

urlpatterns = [
    path('', include(router.urls)),
    path('kosts/<int:kost_pk>/payment-methods/', PaymentMethodViewSet.as_view({'get': 'list', 'post': 'create'}), name='kost-payment-methods-list'),
    path('kosts/<int:kost_pk>/payment-methods/<int:pk>/', PaymentMethodViewSet.as_view({'get': 'retrieve', 'delete': 'destroy'}), name='kost-payment-methods-detail'),
]