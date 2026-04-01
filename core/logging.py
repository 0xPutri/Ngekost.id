import contextvars
import json
import logging
from collections.abc import Mapping, Sequence


REQUEST_CONTEXT = {
    'request_id': contextvars.ContextVar('request_id', default='-'),
    'method': contextvars.ContextVar('method', default='-'),
    'path': contextvars.ContextVar('path', default='-'),
    'user_id': contextvars.ContextVar('user_id', default='-'),
    'user_role': contextvars.ContextVar('user_role', default='-'),
    'client_ip': contextvars.ContextVar('client_ip', default='-'),
}

SENSITIVE_KEYWORDS = {
    'password',
    'password_confirm',
    'token',
    'access',
    'refresh',
    'authorization',
    'secret',
    'api_key',
    'secret_key',
    'credential',
    'session',
    'cookie',
}

MASKED_KEYWORDS = {
    'email',
    'username',
    'phone',
    'phone_number',
}

DEFAULT_LOG_RECORD_FIELDS = set(logging.makeLogRecord({}).__dict__.keys())


def set_request_context(**kwargs):
    for key, value in kwargs.items():
        context_var = REQUEST_CONTEXT.get(key)
        if context_var is not None:
            context_var.set(value if value not in (None, '') else '-')


def clear_request_context():
    for context_var in REQUEST_CONTEXT.values():
        context_var.set('-')


def get_request_context():
    return {key: context_var.get() for key, context_var in REQUEST_CONTEXT.items()}


def get_client_ip(request):
    forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if forwarded_for:
        return forwarded_for.split(',')[0].strip()
    return request.META.get('REMOTE_ADDR', '-')


def _contains_keyword(value, keywords):
    lower_value = str(value).lower()
    return any(keyword in lower_value for keyword in keywords)


def _mask_string(value):
    if not value:
        return value

    string_value = str(value)
    if '@' in string_value:
        local_part, domain = string_value.split('@', 1)
        if len(local_part) <= 2:
            return f"{local_part[0]}***@{domain}" if local_part else f"***@{domain}"
        return f"{local_part[:2]}***@{domain}"

    if len(string_value) <= 2:
        return '*' * len(string_value)
    if len(string_value) <= 6:
        return f"{string_value[:1]}***{string_value[-1:]}"
    return f"{string_value[:2]}***{string_value[-2:]}"


def sanitize_log_data(data, parent_key=''):
    if isinstance(data, Mapping):
        sanitized = {}
        for key, value in data.items():
            key_name = str(key)
            normalized_key = key_name.lower()
            full_key = f'{parent_key}.{normalized_key}' if parent_key else normalized_key

            if _contains_keyword(full_key, SENSITIVE_KEYWORDS):
                sanitized[key_name] = '[DISAMARKAN]'
                continue

            if _contains_keyword(full_key, MASKED_KEYWORDS):
                sanitized[key_name] = _mask_string(value)
                continue

            sanitized[key_name] = sanitize_log_data(value, parent_key=full_key)
        return sanitized

    if isinstance(data, Sequence) and not isinstance(data, (str, bytes, bytearray)):
        return [sanitize_log_data(item, parent_key=parent_key) for item in data]

    return data


class RequestContextFilter(logging.Filter):
    def filter(self, record):
        context = get_request_context()
        record.request_id = context['request_id']
        record.http_method = context['method']
        record.request_path = context['path']
        record.user_id = context['user_id']
        record.user_role = context['user_role']
        record.client_ip = context['client_ip']
        return True


class SafeExtraFormatter(logging.Formatter):
    def format(self, record):
        extra_fields = {}
        for key, value in record.__dict__.items():
            if key in DEFAULT_LOG_RECORD_FIELDS:
                continue
            if key in {
                'request_id',
                'http_method',
                'request_path',
                'user_id',
                'user_role',
                'client_ip',
            }:
                continue
            if key.startswith('_'):
                continue
            extra_fields[key] = value

        record.extra_data = '-'
        if extra_fields:
            record.extra_data = json.dumps(
                sanitize_log_data(extra_fields),
                ensure_ascii=False,
                sort_keys=True,
                default=str,
            )

        return super().format(record)
