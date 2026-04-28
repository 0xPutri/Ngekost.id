import pytest
from django.contrib.auth import get_user_model

User = get_user_model()

@pytest.mark.django_db
class TestUserModel:
    """
    Kumpulan pengujian untuk model pengguna (CustomUser).

    Kelas ini memastikan bahwa sistem autentikasi dan profil pengguna
    berjalan sesuai dengan aturan bisnis yang ditetapkan.
    """

    def test_create_user(self, user_factory):
        """
        Memastikan pengguna berhasil dibuat dengan identitas yang benar.

        Fungsi ini memvalidasi apakah peran (role) dan format string
        dari pengguna Hanna Fernanda sudah sesuai.
        """
        user = user_factory(username="hanna_test", role="owner")
        assert user.username == "hanna_test"
        assert user.role == "owner"
        assert user.get_role_display() == "Owner"
        assert str(user) == "hanna_test (Owner)"

    def test_user_email_uniqueness(self, user_factory):
        """
        Memvalidasi aturan keunikan alamat email pengguna.

        Sistem harus menolak pembuatan akun baru jika menggunakan email
        yang sudah terdaftar sebelumnya di database.
        """
        user_factory(username="user1", email="same@example.com")
        with pytest.raises(Exception):
            user_factory(username="user2", email="same@example.com")