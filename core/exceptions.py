import logging
import uuid
from django.conf import settings
from django.http import JsonResponse
from rest_framework.views import exception_handler as drf_exception_handler
from .logging import get_client_ip


logger = logging.getLogger('ngekost.api')


def custom_exception_handler(exc, context):
    """
    Menangani exception DRF yang masih dapat dikembalikan secara terkelola.

    Fungsi ini menambahkan pencatatan log pada galat API tanpa mengubah
    payload respons standar yang sudah dibentuk DRF.

    Args:
        exc (Exception): Exception yang dilempar selama proses request.
        context (dict): Konteks request dan view dari DRF.

    Returns:
        Response | None: Respons galat dari DRF, atau `None` jika tidak ditangani.
    """
    response = drf_exception_handler(exc, context)

    if response is None:
        return response

    request = context.get('request')
    view = context.get('view')
    response_data = response.data if isinstance(response.data, dict) else {}

    logger.log(
        logging.ERROR if response.status_code >= 500 else logging.WARNING,
        'API mengembalikan respons galat terkelola.',
        extra={
            'status_code': response.status_code,
            'view': view.__class__.__name__ if view else '-',
            'method': request.method if request else '-',
            'path': request.path if request else '-',
            'jenis_exception': exc.__class__.__name__,
            'field_error': sorted(response_data.keys()),
        },
    )

    return response


def _build_error_payload(pesan, status_code, request_id):
    """
    Membentuk payload galat JSON yang konsisten untuk seluruh aplikasi.

    Args:
        pesan (str): Pesan galat yang akan ditampilkan ke klien.
        status_code (int): Kode status HTTP terkait.
        request_id (str): Penanda request untuk kebutuhan pelacakan.

    Returns:
        dict: Payload galat yang siap dikirim sebagai respons.
    """
    payload = {
        'status': 'gagal',
        'pesan': pesan,
        'request_id': request_id,
    }

    if settings.DEBUG:
        payload['kode_status'] = status_code

    return payload


def build_unhandled_exception_response(request, exc, request_id):
    """
    Membentuk respons saat terjadi galat global yang tidak tertangani.

    Args:
        request (HttpRequest): Request yang sedang diproses.
        exc (Exception): Exception yang memicu galat server.
        request_id (str): Penanda request untuk pelacakan log.

    Returns:
        JsonResponse: Respons HTTP 500 yang aman untuk klien.
    """
    logger.exception(
        'Terjadi galat global yang tidak tertangani.',
        extra={
            'status_code': 500,
            'method': request.method if request else '-',
            'path': request.path if request else '-',
            'client_ip': get_client_ip(request) if request else '-',
            'jenis_exception': exc.__class__.__name__,
        },
    )

    return JsonResponse(
        _build_error_payload(
            'Terjadi kesalahan internal pada server. Silakan coba beberapa saat lagi.',
            500,
            request_id,
        ),
        status=500,
    )


def bad_request_handler(request, exception):
    """
    Menangani respons global untuk kesalahan HTTP 400.

    Args:
        request (HttpRequest): Request yang memicu galat.
        exception (Exception): Exception yang diterima Django.

    Returns:
        JsonResponse: Respons JSON standar untuk permintaan tidak valid.
    """
    request_id = request.headers.get('X-Request-ID', str(uuid.uuid4()))
    logger.warning(
        'Permintaan tidak valid.',
        extra={
            'status_code': 400,
            'method': request.method,
            'path': request.path,
            'client_ip': get_client_ip(request),
            'jenis_exception': exception.__class__.__name__,
        },
    )
    return JsonResponse(
        _build_error_payload('Permintaan tidak valid.', 400, request_id),
        status=400,
    )


def permission_denied_handler(request, exception):
    """
    Menangani respons global untuk kesalahan HTTP 403.

    Args:
        request (HttpRequest): Request yang memicu galat.
        exception (Exception): Exception yang diterima Django.

    Returns:
        JsonResponse: Respons JSON standar untuk akses yang ditolak.
    """
    request_id = request.headers.get('X-Request-ID', str(uuid.uuid4()))
    logger.warning(
        'Akses ke sumber daya ditolak.',
        extra={
            'status_code': 403,
            'method': request.method,
            'path': request.path,
            'client_ip': get_client_ip(request),
            'jenis_exception': exception.__class__.__name__,
        },
    )
    return JsonResponse(
        _build_error_payload(
            'Anda tidak memiliki izin untuk mengakses sumber daya ini.',
            403,
            request_id,
        ),
        status=403,
    )


def not_found_handler(request, exception):
    """
    Menangani respons global untuk kesalahan HTTP 404.

    Args:
        request (HttpRequest): Request yang memicu galat.
        exception (Exception): Exception yang diterima Django.

    Returns:
        JsonResponse: Respons JSON standar untuk rute yang tidak ditemukan.
    """
    request_id = request.headers.get('X-Request-ID', str(uuid.uuid4()))
    logger.warning(
        'Rute yang diminta tidak ditemukan.',
        extra={
            'status_code': 404,
            'method': request.method,
            'path': request.path,
            'client_ip': get_client_ip(request),
            'jenis_exception': exception.__class__.__name__,
        },
    )
    return JsonResponse(
        _build_error_payload('Rute atau sumber daya yang diminta tidak ditemukan.', 404, request_id),
        status=404,
    )


def server_error_handler(request):
    """
    Menangani fallback respons global untuk kesalahan HTTP 500.

    Args:
        request (HttpRequest): Request yang sedang diproses.

    Returns:
        JsonResponse: Respons JSON standar untuk kesalahan server.
    """
    request_id = request.headers.get('X-Request-ID', str(uuid.uuid4()))
    logger.error(
        'Handler 500 Django dipanggil.',
        extra={
            'status_code': 500,
            'method': request.method if request else '-',
            'path': request.path if request else '-',
            'client_ip': get_client_ip(request) if request else '-',
        },
    )
    return JsonResponse(
        _build_error_payload(
            'Terjadi kesalahan internal pada server. Silakan coba beberapa saat lagi.',
            500,
            request_id,
        ),
        status=500,
    )