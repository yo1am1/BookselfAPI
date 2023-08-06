from rest_framework.permissions import BasePermission


class IsAuthenticatedOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        return (
            request.method in ("GET", "HEAD", "OPTIONS")
            or request.user.is_authenticated
        )
