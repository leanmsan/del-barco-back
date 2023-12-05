from functools import wraps
from django.http import JsonResponse
from rest_framework_simplejwt.tokens import TokenError, AccessToken
from rest_framework_simplejwt.exceptions import InvalidToken

def get_token_from_request(request):
    auth_header = request.headers.get('Authorization', None)
    if auth_header is not None:
        try:
            _, token = auth_header.split()
            return token
        except ValueError:
            # Manejar el caso en que no se pueda dividir el encabezado de autorización
            return None
    return None

def authentication_required(view_func):
    @wraps(view_func)
    def _wrapped_view(self, request, *args, **kwargs):
        token = get_token_from_request(request)
        if token:
            try:
                AccessToken(token)
                return view_func(self, request, *args, **kwargs)
            except InvalidToken:
                return JsonResponse({'message': 'Token inválido'}, status=401)
            except TokenError as e:
                return JsonResponse({'message': f'Error de token: {e}'}, status=401)
        else:
            return JsonResponse({'message': 'Credenciales de autenticación no proporcionadas'}, status=401)
    return _wrapped_view
