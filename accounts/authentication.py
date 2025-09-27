# accounts/authentication.py
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework import exceptions

class CookieJWTAuthentication(JWTAuthentication):
    def authenticate(self, request):
        # Look for the access token in the cookie
        access_token = request.COOKIES.get("access_token")
        if not access_token:
            return None  # No token, return None so IsAuthenticated fails
        # Set the header manually so JWTAuthentication can parse it
        request.META["HTTP_AUTHORIZATION"] = f"Bearer {access_token}"
        return super().authenticate(request)
