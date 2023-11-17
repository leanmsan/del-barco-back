from django.urls import path
from .views import RegisterUserView, VerifyUserEmail, LoginUserView, TestAuthenticationView, PasswordResetConfirm, PasswordResetRequestView, SetNewPassword, LogoutUserView

urlpatterns = [
    path('register/', RegisterUserView.as_view(), name='register'),
    path('verify-email/', VerifyUserEmail.as_view(), name='verify'),
    path('login/', LoginUserView.as_view(), name='login'),
    path('profile/', TestAuthenticationView.as_view(), name='granted'),
    path('password-reset/', PasswordResetRequestView.as_view(), name='password-reset'),
    path('api/password-reset-confirm/<str:uidb64>/<str:token>/', PasswordResetConfirm.as_view(), name='password-reset-confirm'),
    path('change-password/', SetNewPassword.as_view(), name='change-password'),
    path('logout/', LogoutUserView.as_view(), name='logout'),
]
