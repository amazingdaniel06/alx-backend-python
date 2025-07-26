import logging
from datetime import datetime, timedelta
from django.http import HttpResponseForbidden
from django.utils.deprecation import MiddlewareMixin
from django.core.cache import cache

# Configure the logger for request logging
logging.basicConfig(
    filename='requests.log',
    level=logging.INFO,
    format='%(message)s',
)

class RequestLoggingMiddleware(MiddlewareMixin):
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        user = request.user if request.user.is_authenticated else 'Anonymous'
        log_message = f"{datetime.now()} - User: {user} - Path: {request.path}"
        logging.info(log_message)
        return self.get_response(request)


class RestrictAccessByTimeMiddleware(MiddlewareMixin):
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        current_hour = datetime.now().hour
        # Block access before 6PM (18) and after 9PM (21)
        if request.path.startswith('/chats/') and (current_hour < 18 or current_hour >= 21):
            return HttpResponseForbidden("Chat is only available between 6PM and 9PM.")
        return self.get_response(request)


class OffensiveLanguageMiddleware(MiddlewareMixin):
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.method == 'POST' and request.path.startswith('/chats/'):
            ip = self.get_client_ip(request)
            cache_key = f"msg_count_{ip}"
            count, expires = cache.get(cache_key, (0, datetime.now() + timedelta(minutes=1)))
            if datetime.now() > expires:
                count = 0
                expires = datetime.now() + timedelta(minutes=1)
            if count >= 5:
                return HttpResponseForbidden("Rate limit exceeded. Max 5 messages per minute.")
            cache.set(cache_key, (count + 1, expires), timeout=60)
        return self.get_response(request)

    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        return x_forwarded_for.split(',')[0] if x_forwarded_for else request.META.get('REMOTE_ADDR')


class RolepermissionMiddleware(MiddlewareMixin):
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.path.startswith('/chats/') and request.method in ['POST', 'PUT', 'DELETE']:
            user = request.user
            if not user.is_authenticated or user.role not in ['admin', 'moderator']:
                return HttpResponseForbidden("Only admins or moderators can perform this action.")
        return self.get_response(request)
