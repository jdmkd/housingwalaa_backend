import random
from datetime import timedelta
from django.utils import timezone
from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password, ValidationError
from rest_framework import generics, status, permissions, throttling
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenRefreshView

from accounts.authentication import CookieJWTAuthentication
from .models import User, OTP
from .serializers import (
    SendOTPSerializer,
    VerifyOTPSerializer,
    RegisterSerializer,
    LoginSerializer,
    ForgotPasswordSerializer,
    ResetPasswordSerializer,
)
from core.response_utils import success_response, error_response


# ----- Throttling -----
class OTPThrottle(throttling.UserRateThrottle):
    scope = 'otp'
    rate = '5/min'  # max 5 OTP requests per minute per IP


# ----- OTP sending stub -----
def send_otp_via_whatsapp(phone_number, otp_code):
    print(f"Sending WhatsApp OTP to {phone_number}: {otp_code}")


# ----- Send OTP -----
class SendOTPView(APIView):
    permission_classes = [permissions.AllowAny]
    throttle_classes = [OTPThrottle]

    def post(self, request):
        serializer = SendOTPSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        phone_number = serializer.validated_data["phone_number"]

        # Invalidate old OTPs
        OTP.objects.filter(phone_number=phone_number, is_used=False).update(is_used=True)

        # Generate fresh OTP
        otp_code = OTP.generate_otp()
        OTP.objects.create(phone_number=phone_number, code=otp_code)

        send_otp_via_whatsapp(phone_number, otp_code)
        # send_otp(phone_number, otp_code)

        return success_response(
            message="OTP sent successfully",
            special_code="otp_sent_successful"
        )


# ----- Verify OTP -----
class VerifyOTPView(APIView):
    permission_classes = [permissions.AllowAny]
    throttle_classes = [OTPThrottle]

    def post(self, request):
        serializer = VerifyOTPSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        phone_number = serializer.validated_data["phone_number"]
        otp_code = serializer.validated_data["otp"]

        try:
            otp = OTP.objects.filter(phone_number=phone_number, code=otp_code, is_used=False).latest('created_at')
        except OTP.DoesNotExist:
            return error_response(
                message="Invalid OTP",
                special_code="otp_invalid",
                status_code=status.HTTP_400_BAD_REQUEST
            )

        if not otp.is_valid():
            otp.is_used = True
            otp.save()

            # Auto-generate + send new OTP
            new_code = OTP.generate_otp()
            OTP.objects.create(phone_number=phone_number, code=new_code)
            send_otp_via_whatsapp(phone_number, new_code)

            return success_response(
                message="OTP expired. A new one has been sent.",
                special_code="otp_expired_resent"
            )

        # Mark OTP as used
        otp.is_used = True
        otp.save()

        # Mark user as verified
        try:
            user = User.objects.get(phone_number=phone_number)
            user.is_verified = True
            user.save()
        except User.DoesNotExist:
            return error_response(
                message="User not found",
                special_code="user_not_found",
                status_code=status.HTTP_404_NOT_FOUND
            )

        return success_response(
            message="Account verified successfully",
            special_code="otp_verified_successful"
        )


# ----- Register User -----
class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]
    throttle_classes = [OTPThrottle]

    # def perform_create(self, serializer):
    #     user = serializer.save()
    #     otp_code = OTP.generate_otp()
    #     OTP.objects.create(phone_number=user.phone_number, code=otp_code)
    #     send_otp_via_whatsapp(user.phone_number, otp_code)
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        
        try:
            serializer.is_valid(raise_exception=True)
        except ValidationError as exc:
            return error_response(
                message="Validation failed",
                errors=exc.detail,  # {"phone_number": [...]} or {"password": [...]}
                special_code="VALIDATION_ERROR",
                status_code=status.HTTP_400_BAD_REQUEST,
            )
        
        user = serializer.save()

        # Generate & send OTP
        otp_code = OTP.generate_otp()
        OTP.objects.create(phone_number=user.phone_number, code=otp_code)
        send_otp_via_whatsapp(user.phone_number, otp_code)

        # Standard response structure
        return success_response(
            data={
                "id": user.id,
                "full_name": user.full_name,
                "phone_number": user.phone_number,
                "is_verified": user.is_verified,
            },
            message = "Registration successful. OTP sent for verification.",
            special_code = "REGISTRATION_SUCCESS",
            status_code=status.HTTP_201_CREATED,
        )
    

# ----- Login User -----
class LoginView(generics.GenericAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]

        if not user.is_verified:
            return error_response(
                message="Account not verified. OTP required.",
                special_code="login_unverified",
                status_code=status.HTTP_403_FORBIDDEN
            )

        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)
        refresh_token = str(refresh)

        response = success_response(
            data={
                "user": {
                    "id": user.id,
                    "full_name": user.full_name,
                    "phone_number": user.phone_number,
                    "is_verified": user.is_verified,
                }
            },
            message="Login successful",
            special_code="login_successful"
        )

        # Set tokens in HttpOnly cookies
        response.set_cookie(
            key="access_token",
            value=access_token,
            httponly=True,
            secure=True,         # True on production HTTPS
            # samesite="Strict",    # CSRF protection
            samesite="None",
            max_age=60 * 5,          # 5 minutes
        )
        response.set_cookie(
            key="refresh_token",
            value=refresh_token,
            httponly=True,
            secure=True,
            samesite="None",
            max_age=60 * 60 * 24 * 7,  # 7 days
        )
        response.set_cookie(
            key="session_exists",
            value="true",  # signed on server optionally
            httponly=False,  # readable by JS
            secure=True,
            samesite="None",
            max_age=60 * 15,  # 15 min
        )

        return response


class LogoutView(APIView):
    authentication_classes = [CookieJWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        response = success_response(
            message="Logged out successfully",
            special_code="logout_successful"
        )
        
        # response.delete_cookie("access_token")
        response.delete_cookie("access_token", path="/", samesite="None")
        response.delete_cookie("refresh_token", path='/', samesite="None")
        response.delete_cookie("session_exists", path='/', samesite="None")

        return response




class CookieTokenRefreshView(TokenRefreshView):
    def post(self, request, *args, **kwargs):
        refresh_token = request.COOKIES.get("refresh_token")

        if not refresh_token:
            return error_response(
                message="Refresh token missing",
                special_code="refresh_token_missing",
                status_code=status.HTTP_401_UNAUTHORIZED
            )
        
        try:
            token = RefreshToken(refresh_token)
            access_token = str(token.access_token)
        except Exception:
            return Response({"detail": "Invalid refresh token"}, status=401)

        # request.data["access_token"] = access_token
        # request.data["refresh_token"] = refresh_token
        # response = super().post(request, *args, **kwargs)

        response = success_response(
            message="Token refreshed successfully",
            special_code="token_refresh_successful"
        )

        response.set_cookie(
            "access_token",
            access_token,
            httponly=True,
            secure=True,
            samesite="None",
            max_age=60 * 5
        )
        response.set_cookie(
            "session_exists",
            "true",
            httponly=False,
            secure=True,
            samesite="None",
            max_age=60*15
        )

        return response

    
class MeView(APIView):
    authentication_classes = [CookieJWTAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self, request):
        user = request.user
        return success_response(
            data={
                "id": user.id,
                "phone_number": user.phone_number,
                "username": user.username,
                "full_name": user.full_name,
            },
            message="User profile fetched",
            special_code="profile_fetched"
        )


# ----- Forgot Password -----
class ForgotPasswordView(APIView):
    permission_classes = [permissions.AllowAny]
    throttle_classes = [OTPThrottle]

    def post(self, request):
        serializer = ForgotPasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        phone_number = serializer.validated_data["phone_number"]

        otp_code = OTP.generate_otp()
        OTP.objects.create(phone_number=phone_number, code=otp_code)

        send_otp_via_whatsapp(phone_number, otp_code)
        
        return success_response(
            message="OTP sent for password reset",
            special_code="forgot_password_otp_sent"
        )


# ----- Reset Password -----
class ResetPasswordView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = ResetPasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return success_response(
            message="Password reset successfully",
            special_code="password_reset_successful"
        )


# ----- Example Protected Endpoint -----
class ProfileView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        user = request.user
        
        return success_response(
            data={
                "id": user.id,
                "full_name": user.full_name,
                "phone_number": user.phone_number
            },
            message="Profile fetched",
            special_code="profile_fetched"
        )