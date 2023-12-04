from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import GenericAPIView
from .serializers import UserRegisterSerializer, UserSerializer, LoginSerializer, PasswordResetRequestSerializer, SetNewPasswordSerializer, LogoutSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .utils import send_code_to_user
from .models import User, OneTimePassword
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import smart_str
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from rest_framework.exceptions import ValidationError


class RegisterUserView(GenericAPIView):
    serializer_class=UserRegisterSerializer
    #permission_classes = [IsAuthenticated]

    def post(self, request):
        user_data = request.data
        serializer = self.serializer_class(data=user_data)

        if serializer.is_valid(raise_exception=True):
            serializer.save()
            user = serializer.data

            #send email function user['email']
            send_code_to_user(user['email'])

            return Response({
                'data': user,
                'message': f'Hola {user["first_name"]} bienvenido a Del Barco!'
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class UserDetailsAPIView(APIView):
    #permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)

class UserDeleteAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request):
        user = request.user

        # Verificar si el usuario existe antes de intentar eliminar
        if user:
            user.delete()
            return Response({'message': 'Usuario eliminado correctamente'}, status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({'message': 'Usuario no encontrado'}, status=status.HTTP_404_NOT_FOUND)

class VerifyUserEmail(GenericAPIView):
    def post(self, request):
        otpcode = request.data.get('otp')
        try: 
            user_code_obj = OneTimePassword.objects.get(code=otpcode)
            user = user_code_obj.user
            if not user.is_verified:
                user.is_verified = True
                user.save()
                return Response({
                    'message': 'Email verificado correctamente!'
                }, status=status.HTTP_200_OK)
            return Response({
                'message': 'El email ya ha sido verificado'
            }, status=status.HTTP_204_NO_CONTENT)
        except OneTimePassword.DoesNotExist:
            return Response({
                'message': 'passcode not provided'
            }, status=status.HTTP_404_NOT_FOUND)
        
class LoginUserView(GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class TestAuthenticationView(GenericAPIView):
    permission_classes = [IsAuthenticated]

    def get(self, reques):
        data= {
            'message': 'its works'
        }
        return Response(data, status=status.HTTP_200_OK)
    
class PasswordResetRequestView(GenericAPIView):
    serializer_class = PasswordResetRequestSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)

        return Response({'message': "Te enviamos un link para cambiar tu contraseña"}, status=status.HTTP_200_OK)
    
class PasswordResetConfirm(GenericAPIView):
    def get(self, request, uidb64, token):
        try:
            user_id = smart_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(id=user_id)
            
            if not PasswordResetTokenGenerator().check_token(user, token):
                return Response({'message': "token is invalid or has expired"}, status=status.HTTP_401_UNAUTHORIZED)
            return Response({'success': True, 'message': "credentials are valid", 'uidb64': uidb64, 'token': token}, status=status.HTTP_200_OK)
        except:
            return Response({'message': "Te enviamos un link para cambiar tu contraseña"}, status=status.HTTP_200_OK)
        
class SetNewPassword(APIView):
    def patch(self, request):
        try:
            serializer = SetNewPasswordSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            return Response({'message': "Password reset successfully"}, status=status.HTTP_200_OK)
        except ValidationError as e:
            if "Password do not match" in str(e):
                # Manejar el error de contraseñas que no coinciden
                return Response({'non_field_errors': ['Las contraseñas no coinciden']}, status=status.HTTP_400_BAD_REQUEST)
            else:
                # Mantener el manejo original para otros errores
                return Response({'non_field_errors': [str(e)]}, status=status.HTTP_400_BAD_REQUEST)
    
class LogoutUserView(GenericAPIView):
    serializer_class = LogoutSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(status=status.HTTP_204_NO_CONTENT)
