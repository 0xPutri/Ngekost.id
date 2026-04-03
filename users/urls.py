from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from drf_spectacular.utils import extend_schema
from .views import CustomTokenObtainPairView, RegisterView, UserProfileView

app_name = 'users'

documented_token_refresh_view = extend_schema(
    tags=['Autentikasi'],
    summary='Refresh access token',
    description=(
        'Menerima `refresh token` yang masih valid dan mengembalikan `access token` '
        'baru tanpa meminta kredensial ulang.'
    ),
)(TokenRefreshView)

urlpatterns = [
    # Auth Endpoints
    path('auth/register/', RegisterView.as_view(), name='register'),
    path('auth/login/', CustomTokenObtainPairView.as_view(), name='login'),
    path('auth/refresh/', documented_token_refresh_view.as_view(), name='token_refresh'),

    # Profile Endpoint
    path('profile/', UserProfileView.as_view(), name='profile'),
]