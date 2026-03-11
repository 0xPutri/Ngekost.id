from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AdminUserViewSet, AdminKostViewSet, AdminBookingViewSet

app_name = 'core_admin'

router = DefaultRouter()
router.register(r'users', AdminUserViewSet, basename='admin-user')
router.register(r'kosts', AdminKostViewSet, basename='admin-kost')
router.register(r'bookings', AdminBookingViewSet, basename='admin-booking')

urlpatterns = [
    path('admin-panel/', include(router.urls)),
]