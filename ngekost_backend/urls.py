from django.contrib import admin
from django.urls import path, include
from django.http import JsonResponse
from django.conf import settings
from django.conf.urls.static import static
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView

handler400 = 'core.exceptions.bad_request_handler'
handler403 = 'core.exceptions.permission_denied_handler'
handler404 = 'core.exceptions.not_found_handler'
handler500 = 'core.exceptions.server_error_handler'

def api_root_view(request):
    """
    Menyediakan endpoint dasar untuk mengecek status API.

    Endpoint ini berguna sebagai penanda bahwa layanan backend Ngekost.id
    berjalan dan siap menerima request berikutnya.

    Args:
        request (HttpRequest): Request yang masuk ke root API.

    Returns:
        JsonResponse: Respons status sederhana dari layanan API.
    """
    return JsonResponse({
        "status": "sukses",
        "pesan": "API Ngekost.id berjalan dengan baik.",
        "versi": "1.0"
    })

urlpatterns = [
    path('', api_root_view, name='api-root'),

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

if getattr(settings, 'ENABLE_DJANGO_ADMIN', False):
    urlpatterns.insert(1, path('admin/', admin.site.urls))

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)