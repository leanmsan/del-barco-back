from functools import wraps
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from rest_framework_simplejwt.tokens import TokenError, AccessToken

def get_token_from_request(request):
    auth_header = request.headers.get('Authorization', None)
    if auth_header is not None:
        _, token = auth_header.split()
        return token
    return None

def authentication_required(view_func):
    @wraps(view_func)
    def _wrapped_view(self, request, *args, **kwargs):
        token = get_token_from_request(request)
        if token: 
            try:
                AccessToken(token)
                return view_func(self, request, *args, **kwargs)
            except TokenError as e:
                return JsonResponse({'message': 'Token inválido o expirado'}, status=401)
        else:
            return JsonResponse({'message': 'Authentication credentials were not provided'}, status=401)
    return _wrapped_view