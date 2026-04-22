from django.core.exceptions import FieldDoesNotExist
from django.db.models.fields.related_descriptors import ForwardManyToOneDescriptor

class RoleBasedModelAdminMixin:
    """
    Mengelola hak akses pengguna pada panel Dasbor Ngekost.id.

    Kelas ini memberikan akses penuh untuk admin, sekaligus membatasi owner 
    agar hanya bisa melihat dan mengelola data miliknya sendiri.
    """
    owner_field_path = 'owner'

    def has_module_permission(self, request):
        """
        Memeriksa apakah modul boleh ditampilkan di menu samping dasbor.

        Args:
            request (HttpRequest): Objek request dari klien.

        Returns:
            bool: Mengembalikan True jika pengguna adalah admin atau owner.
        """
        if hasattr(request.user, 'role'):
            if request.user.role == 'admin':
                return True
            if request.user.role == 'owner' and self.owner_field_path is not None:
                return True
        return super().has_module_permission(request)

    def _is_owner_of_obj(self, request, obj):
        """
        Memastikan objek data benar-benar milik owner yang sedang masuk.

        Args:
            request (HttpRequest): Objek request dari klien.
            obj (Any): Objek data yang sedang diperiksa.

        Returns:
            bool: Mengembalikan True jika pemilik data sesuai dengan pengguna.
        """
        if self.owner_field_path is None:
            return False
            
        owner_obj = obj
        for part in self.owner_field_path.split('__'):
            if owner_obj is None:
                return False
            owner_obj = getattr(owner_obj, part, None)
        return owner_obj == request.user

    def has_view_permission(self, request, obj=None):
        """
        Memeriksa izin pengguna untuk melihat detail suatu data.

        Args:
            request (HttpRequest): Objek request dari klien.
            obj (Any, optional): Objek data yang ingin dilihat.

        Returns:
            bool: Mengembalikan True jika pengguna berhak melihat data.
        """
        if hasattr(request.user, 'role'):
            if request.user.role == 'admin':
                return True
            if request.user.role == 'owner':
                if self.owner_field_path is None:
                    return False
                if obj is not None and not self._is_owner_of_obj(request, obj):
                    return False
                return True
        return super().has_view_permission(request, obj)

    def has_add_permission(self, request):
        """
        Memeriksa izin pengguna untuk menambahkan data baru.

        Args:
            request (HttpRequest): Objek request dari klien.

        Returns:
            bool: Mengembalikan True jika pengguna diizinkan menambah data.
        """
        if hasattr(request.user, 'role'):
            if request.user.role == 'admin':
                return True
            if request.user.role == 'owner' and self.owner_field_path is not None:
                return True
        return super().has_add_permission(request)

    def has_change_permission(self, request, obj=None):
        """
        Memeriksa izin pengguna untuk mengubah data yang sudah ada.

        Args:
            request (HttpRequest): Objek request dari klien.
            obj (Any, optional): Objek data yang ingin diubah.

        Returns:
            bool: Mengembalikan True jika pengguna berhak mengubah data.
        """
        return self.has_view_permission(request, obj)

    def has_delete_permission(self, request, obj=None):
        """
        Memeriksa izin pengguna untuk menghapus suatu data.

        Args:
            request (HttpRequest): Objek request dari klien.
            obj (Any, optional): Objek data yang ingin dihapus.

        Returns:
            bool: Mengembalikan True jika pengguna berhak menghapus data.
        """
        return self.has_view_permission(request, obj)

    def get_queryset(self, request):
        """
        Menyaring daftar data agar sesuai dengan hak akses pengguna.

        Fungsi ini memastikan owner hanya dapat melihat daftar properti 
        atau transaksi yang dikelolanya.

        Args:
            request (HttpRequest): Objek request dari klien.

        Returns:
            QuerySet: Daftar data yang sudah disaring.
        """
        qs = super().get_queryset(request)
        if hasattr(request.user, 'role') and request.user.role == 'owner':
            if self.owner_field_path is None:
                return qs.none()
            return qs.filter(**{self.owner_field_path: request.user})
        return qs