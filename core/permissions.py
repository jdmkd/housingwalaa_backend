from rest_framework import permissions

class IsAuthenticatedOrReadOnly(permissions.BasePermission):
    """
    Allow anyone to read (GET, HEAD, OPTIONS),
    but only authenticated users can POST/PUT/DELETE.
    """
    def has_permission(self, request, view):
        # Safe methods: GET, HEAD, OPTIONS
        if request.method in permissions.SAFE_METHODS:
            return True
        # Other methods require authentication
        return request.user and request.user.is_authenticated
