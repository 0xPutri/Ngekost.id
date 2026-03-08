from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import KostViewSet, RoomViewSet

app_name = 'kosts'

router = DefaultRouter()
router.register(r'kosts', KostViewSet, basename='kost')
router.register(r'rooms', RoomViewSet, basename='room')

urlpatterns = [
    path('', include(router.urls)),
]