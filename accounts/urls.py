from django.urls import path, include
from .views import CookieTokenRefreshView, ForgotPasswordView, LoginView, LogoutView, MeView, ProfileView, RegisterView, ResetPasswordView, SendOTPView, VerifyOTPView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView

urlpatterns = [
    path("auth/register/", RegisterView.as_view(), name="register"),
    path("auth/login/", LoginView.as_view(), name="login"),
    path("auth/logout/", LogoutView.as_view(), name="logout"),
    path("auth/me/", MeView.as_view(), name="me"),

    path("auth/send-otp/", SendOTPView.as_view(), name="send-otp"),
    path("auth/verify-otp/", VerifyOTPView.as_view(), name="verify-otp"),

    path("auth/forgot-password/", ForgotPasswordView.as_view(), name="forgot-password"),
    path("auth/reset-password/", ResetPasswordView.as_view(), name="reset-password"),

    # Protected endpoint example
    path('auth/profile/', ProfileView.as_view(), name='profile'),

    # Cookie-based JWT refresh
    path("auth/token/refresh/", CookieTokenRefreshView.as_view(), name="token_refresh"),

    
    # path('auth/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    # path('auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    # path('auth/token/verify/', TokenVerifyView.as_view(), name='token_verify'),

]
