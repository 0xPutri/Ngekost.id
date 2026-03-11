from django.contrib import admin
from django.urls import path, include
from django.http import JsonResponse
from django.conf import settings
from django.conf.urls.static import static
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView

def api_root_view(request):
    """Root endpoint untuk mengecek status API."""
    return JsonResponse({
        "status": "sukses",
        "pesan": "API Ngekost.id berjalan dengan baik.",
        "versi": "1.0"
    })

urlpatterns = [
    path('', api_root_view, name='api-root'),
    path('admin/', admin.site.urls),

    # Routing Aplikasi (API v1)
    path('api/v1/users/', include('users.urls')),
    path('api/v1/', include('kosts.urls')),
    path('api/v1/', include('transactions.urls')),
    path('api/v1/core/', include('core.urls')),

    # API Documentation
    path('api/docs/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/swagger/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/docs/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)