from rest_framework import permissions

class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Mengizinkan akses tulis hanya untuk owner yang berwenang.

    Permission ini tetap membuka akses baca untuk publik, tetapi membatasi
    perubahan data kost dan kamar hanya pada pemilik yang sesuai.
    """

    def hasattr_owner(self, obj):
        """
        Mengambil owner dari objek kost atau kamar yang diperiksa.

        Args:
            obj (Any): Objek target permission.

        Returns:
            CustomUser | None: Owner terkait jika ditemukan.
        """
        if hasattr(obj, 'owner'):
            return obj.owner
        elif hasattr(obj, 'kost'):
            return obj.kost.owner
        elif hasattr(obj, 'room'):
            return obj.room.kost.owner
        return None
    
    def has_permission(self, request, view):
        """
        Memeriksa izin dasar sebelum akses objek dijalankan.

        Args:
            request (Request): Request yang sedang diproses.
            view (APIView): View yang memanggil permission.

        Returns:
            bool: `True` untuk akses baca publik atau owner terautentikasi.
        """
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.is_authenticated and request.user.role == 'owner'
    
    def has_object_permission(self, request, view, obj):
        """
        Memeriksa apakah objek dikelola oleh owner yang sedang login.

        Args:
            request (Request): Request yang sedang diproses.
            view (APIView): View yang memanggil permission.
            obj (Any): Objek kost atau kamar yang diakses.

        Returns:
            bool: `True` jika akses baca diizinkan atau owner sesuai.
        """
        if request.method in permissions.SAFE_METHODS:
            return True
        
        owner = self.hasattr_owner(obj)
        return owner == request.user