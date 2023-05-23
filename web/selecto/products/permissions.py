from rest_framework import permissions

class IsAdminOrReadOnly(permissions.IsAdminUser):
    def has_permission(self, request, view):
        # Check if the request method is safe (GET, HEAD, OPTIONS)
        if request.method in permissions.SAFE_METHODS:
            return True

        # For non-safe methods, delegate the permission check to IsAdminUser
        return super().has_permission(request, view)