from rest_framework import permissions

class IsAdminRole(permissions.BasePermission):
    """
    Membatasi akses endpoint hanya untuk pengguna berperan admin.

    Permission ini dipakai pada panel admin API agar data sensitif tetap
    berada di bawah kendali administrator sistem.
    """
    message = "Akses ditolak. Endpoint ini khusus untuk Administrator."

    def has_permission(self, request, view):
        """
        Memeriksa apakah pengguna aktif adalah admin yang terautentikasi.

        Args:
            request (Request): Request yang sedang diproses.
            view (APIView): View yang memanggil permission.

        Returns:
            bool: `True` jika pengguna adalah admin yang valid.
        """
        return bool(request.user and request.user.is_authenticated and request.user.role == 'admin')