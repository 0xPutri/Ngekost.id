import logging
import time
import uuid
from .logging import clear_request_context, get_client_ip, set_request_context


logger = logging.getLogger('ngekost.request')


class RequestContextLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        request_id = request.headers.get('X-Request-ID', str(uuid.uuid4()))
        request._logging_started_at = time.perf_counter()

        user = getattr(request, 'user', None)
        user_id = getattr(user, 'id', '-') if getattr(user, 'is_authenticated', False) else '-'
        user_role = getattr(user, 'role', '-') if getattr(user, 'is_authenticated', False) else '-'

        set_request_context(
            request_id=request_id,
            method=request.method,
            path=request.path,
            user_id=user_id,
            user_role=user_role,
            client_ip=get_client_ip(request),
        )

        logger.info(
            'Permintaan API diterima.',
            extra={
                'query_params': dict(request.GET.lists()),
            },
        )

        try:
            response = self.get_response(request)
        except Exception:
            duration_ms = round((time.perf_counter() - request._logging_started_at) * 1000, 2)
            logger.exception(
                'Terjadi galat tak tertangani saat memproses permintaan API.',
                extra={'durasi_ms': duration_ms},
            )
            clear_request_context()
            raise

        authenticated_user = getattr(request, 'user', None)
        if getattr(authenticated_user, 'is_authenticated', False):
            set_request_context(
                user_id=getattr(authenticated_user, 'id', '-'),
                user_role=getattr(authenticated_user, 'role', '-'),
            )

        duration_ms = round((time.perf_counter() - request._logging_started_at) * 1000, 2)
        logger.info(
            'Permintaan API selesai diproses.',
            extra={
                'status_code': response.status_code,
                'durasi_ms': duration_ms,
            },
        )
        clear_request_context()
        return response