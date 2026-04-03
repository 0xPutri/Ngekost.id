from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import KostImageViewSet, KostViewSet, RoomImageViewSet, RoomViewSet

app_name = 'kosts'

router = DefaultRouter()
router.register(r'kosts', KostViewSet, basename='kost')
router.register(r'rooms', RoomViewSet, basename='room')
router.register(r'kost-images', KostImageViewSet, basename='kost-image')
router.register(r'room-images', RoomImageViewSet, basename='room-image')

urlpatterns = [
    path('', include(router.urls)),
]