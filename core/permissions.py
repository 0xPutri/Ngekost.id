from rest_framework import permissions

class IsAdminRole(permissions.BasePermission):
    message = "Akses ditolak. Endpoint ini khusus untuk Administrator."

    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and request.user.role == 'admin')