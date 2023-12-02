from rest_framework import serializers
from .models import User
from django.contrib.auth import authenticate
from rest_framework.exceptions import AuthenticationFailed
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.utils.encoding import smart_str, smart_bytes, force_str
from rest_framework_simplejwt.tokens import Token, TokenError, RefreshToken

class UserRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=68, min_length=6, write_only=True)
    password2= serializers.CharField(max_length=68, min_length=6, write_only=True)

    class Meta:
        model=User
        fields=['email', 'first_name', 'last_name', 'password', 'password2']
    
    def validate(self, attrs):
        password = attrs.get('password', '')
        password2 = attrs.get('password2', '')
        if password != password2:
            raise serializers.ValidationError("Las contraseñas no coiciden")
        return attrs
    
    def create(self, validated_data):
        user = User.objects.create_user(
            email = validated_data['email'],
            first_name = validated_data.get('first_name'),
            last_name = validated_data.get('last_name'),
            password = validated_data.get('password')
        )
        return user
    
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name']
    
class LoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=255, min_length=6)
    password = serializers.CharField(max_length=68, write_only=True)
    full_name = serializers.CharField(max_length=255, read_only=True)
    access_token = serializers.CharField(max_length=255, read_only=True)
    refresh_token = serializers.CharField(max_length=255, read_only=True)

    class Meta:
        model = User
        fields = ['email', 'password', 'full_name', 'access_token', 'refresh_token']

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')
        request = self.context.get('request')
        user = authenticate(request, email=email, password=password)

        if not user or not user.check_password(password):
            raise AuthenticationFailed("Invalid credentials, please try again")
        if not user.is_verified:
            raise AuthenticationFailed('Email is not verified')
        
        user_token = user.tokens()

        return {
            'email': user.email,
            'full_name': user.get_full_name,
            'access_token': user_token.get('access'),
            'refresh_token': user_token.get('refresh')
        }
    
class PasswordResetRequestSerializer(serializers.Serializer):
    email = serializers.CharField(max_length=255)

    class Meta:
        fields = ['email']

    def validate(self, attrs):
        email = attrs.get('email')

        if User.objects.filter(email=email).exists():
            user = User.objects.get(email=email)
            uidb64 = urlsafe_base64_encode(smart_bytes(user.id))
            token = PasswordResetTokenGenerator().make_token(user)
            request = self.context.get('request')
            site_domain = get_current_site(request).domain
            frontend_url = 'http://localhost:5173/password-reset-confirm/{uidb64}/{token}'
            abslink = frontend_url.format(uidb64=uidb64, token=token)

            # Renderizar el cuerpo del correo electrónico como HTML
            email_body_html = render_to_string('password_reset_email_template.html', {'abslink': abslink, 'user': user})
            
            # Obtener el cuerpo del correo electrónico sin formato HTML para enviar en el formato alternativo
            email_body_text = strip_tags(email_body_html)

            data = {
                'subject': "Recuperar contraseña",
                'message': email_body_text,  # Usar el cuerpo sin formato HTML como texto
                'from_email': 'your_email@example.com',  # Reemplaza con tu dirección de correo
                'recipient_list': [user.email],
                'html_message': email_body_html,  # Agregar el cuerpo HTML al mensaje
            }

            send_mail(**data, fail_silently=False)
        else:
            raise serializers.ValidationError("No se encontró un usuario con esta dirección de correo electrónico.")

        return super().validate(attrs)
    
class SetNewPasswordSerializer(serializers.Serializer):
    password = serializers.CharField(max_length=100, min_length=6, write_only=True)
    confirm_password = serializers.CharField(max_length=100, min_length=6, write_only=True)
    uidb64 = serializers.CharField(write_only=True)
    token = serializers.CharField(write_only=True)

    class Meta:
        fields = ['password', 'confirm_password', 'uidb64', 'token']

    def validate(self, attrs):
        try:
            token = attrs.get('token')
            uidb64 = attrs.get('uidb64')
            password = attrs.get('password')
            confirm_password = attrs.get('confirm_password')

            user_id = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(id=user_id)

            if not PasswordResetTokenGenerator().check_token(user, token):
                raise AuthenticationFailed("Reset link is invalid or expired", 401)

            if password != confirm_password:
                raise serializers.ValidationError("Password do not match")

            user.set_password(password)
            user.save()

            return user
        except Exception as e:
            raise serializers.ValidationError("Link is invalid or has expired")
        
class LogoutSerializer(serializers.Serializer):
    refresh_token = serializers.CharField()

    default_error_messages = {
        'bad_token': ('Token is invalid or has expired')
    }

    def validate(self, attrs):
        self.token = attrs.get('refresh_token')

        return attrs
    
    def save(self, **kwargs):
        try:
            token = RefreshToken(self.token)
            token.blacklist()
        except TokenError:
            return self.fail('bad token')
