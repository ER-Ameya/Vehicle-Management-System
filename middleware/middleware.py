import re
from django.http import HttpResponseForbidden

from django.utils.deprecation import MiddlewareMixin


class XSSMiddleware(MiddlewareMixin):
    def process_request(self, request):
        if request.method == 'POST':
            # Clean POST parameters
            cleaned_data = {}
            for key, value in request.POST.items():
                cleaned_data[key] = self._sanitize(value)
            request.POST = cleaned_data

        return None

    def _sanitize(self, data):
        """
        Sanitize input data to prevent XSS attacks.
        """
        # Remove tags and entities
        data = re.sub('<[^>]*>', '', data)
        data = re.sub('&[^;]+;', '', data)

        return data

    

class IPFilterMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.allowed_ips = ['127.0.0.1'] # Replace with your allowed IPs
        
    def __call__(self, request):
        ip = request.META.get('REMOTE_ADDR')
        if ip not in self.allowed_ips:
            return HttpResponseForbidden('Access denied')
        response = self.get_response(request)
        return response

