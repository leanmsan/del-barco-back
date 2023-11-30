from django.urls import path
from .views import RegisterUserView, UserDetailsAPIView, VerifyUserEmail, UserDeleteAPIView, LoginUserView, TestAuthenticationView, PasswordResetConfirm, PasswordResetRequestView, SetNewPassword, LogoutUserView

urlpatterns = [
    path('register/', RegisterUserView.as_view(), name='register'),
    path('verify-email/', VerifyUserEmail.as_view(), name='verify'),
    path('delete-user/', UserDeleteAPIView.as_view(), name='delete-user'),
    path('login/', LoginUserView.as_view(), name='login'),
    path('profile/', TestAuthenticationView.as_view(), name='granted'),
    path('user-details/', UserDetailsAPIView.as_view(), name='user-details'),
    path('password-reset/', PasswordResetRequestView.as_view(), name='password-reset'),
    path('api/password-reset-confirm/<str:uidb64>/<str:token>/', PasswordResetConfirm.as_view(), name='password-reset-confirm'),
    path('change-password/', SetNewPassword.as_view(), name='change-password'),
    path('logout/', LogoutUserView.as_view(), name='logout'),
]
