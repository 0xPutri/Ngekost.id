import logging
from rest_framework.views import exception_handler as drf_exception_handler


logger = logging.getLogger('ngekost.api')


def custom_exception_handler(exc, context):
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