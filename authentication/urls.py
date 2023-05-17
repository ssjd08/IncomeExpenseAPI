from django.urls import path
from .views import RegisterView, VerifyEmail, LoginAPIView, PasswordTokenCheckAPI, RequestPasswordResetEmail, SetNewPasswordAPIVeiw
from rest_framework_simplejwt.views import TokenRefreshView



urlpatterns = [
    path ('register/', RegisterView.as_view(), name='register'),
    path ('email-verify/', VerifyEmail.as_view(), name='verify_email'),
    path ('login/', LoginAPIView.as_view(), name='login'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path ('password-resrt/<uidb64>/<token>/', PasswordTokenCheckAPI.as_view(), name='password-reset-confirm'), # for pass var too utls we should put var in <>.
    path ('request-resrt-email/', RequestPasswordResetEmail.as_view(), name='request-resrt-email'),
    path ('password-resrt-complete', SetNewPasswordAPIVeiw.as_view(), name='password-resrt-complete'),
]
