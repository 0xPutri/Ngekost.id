from django.contrib import admin
from django.urls import path, include
from django.http import JsonResponse

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

    # Routing Aplikasi Users (API v1)
    path('api/v1/users/', include('users.urls')),

    # Routing Aplikasi Kosts (API v1)
    path('api/v1/', include('kosts.urls')),
]