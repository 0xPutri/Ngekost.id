import pytest
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from kosts.models import Kost, Room, PaymentMethod
from transactions.models import Booking

User = get_user_model()

@pytest.fixture
def api_client():
    """
    Menyediakan klien API untuk kebutuhan pengujian.

    Klien ini digunakan untuk mensimulasikan permintaan HTTP ke berbagai
    endpoint REST API di dalam sistem.

    Returns:
        APIClient: Objek klien yang siap melakukan request.
    """
    return APIClient()

@pytest.fixture
def user_factory(db):
    """
    Membuat fungsi pembantu untuk menghasilkan objek pengguna.

    Fungsi ini memudahkan pembuatan pengguna dengan berbagai peran secara
    cepat dan otomatis untuk kebutuhan test case.

    Returns:
        function: Fungsi untuk membuat instance CustomUser.
    """
    def create_user(username="hannafernanda", role="tenant", password="password123", **kwargs):
        email = kwargs.pop('email', f"{username}@example.com")
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            role=role,
            first_name="Hanna",
            last_name="Fernanda",
            **kwargs
        )
        return user
    return create_user

@pytest.fixture
def owner_user(user_factory):
    """
    Menyediakan pengguna dengan peran sebagai pemilik kost.

    Fixture ini mengembalikan pengguna Hanna Fernanda dengan akses
    sebagai owner untuk pengujian fitur properti.

    Returns:
        CustomUser: Objek pengguna dengan peran owner.
    """
    return user_factory(username="owner_hanna", role="owner")

@pytest.fixture
def tenant_user(user_factory):
    """
    Menyediakan pengguna dengan peran sebagai penyewa kost.

    Fixture ini mengembalikan pengguna Hanna Fernanda dengan akses
    sebagai tenant untuk pengujian fitur booking.

    Returns:
        CustomUser: Objek pengguna dengan peran tenant.
    """
    return user_factory(username="tenant_hanna", role="tenant")

@pytest.fixture
def admin_user(user_factory):
    """
    Menyediakan pengguna dengan peran sebagai administrator.

    Fixture ini menghasilkan akun staf dengan hak akses penuh untuk
    menguji fitur monitoring oleh admin.

    Returns:
        CustomUser: Objek pengguna dengan akses superuser.
    """
    return user_factory(username="admin_hanna", role="admin", is_staff=True, is_superuser=True)

@pytest.fixture
def kost_factory(db, owner_user):
    """
    Membuat fungsi pembantu untuk menghasilkan data kost.

    Fungsi ini menyederhanakan proses penyiapan data properti kost di
    dalam database pengujian.

    Returns:
        function: Fungsi untuk membuat instance Kost.
    """
    def create_kost(name="Kost Sakura", owner=owner_user, **kwargs):
        return Kost.objects.create(
            owner=owner,
            name=name,
            address="Jl. Pendidikan No. 123",
            description="Kost nyaman dan strategis.",
            facilities="WiFi, AC, Kamar Mandi Dalam",
            **kwargs
        )
    return create_kost

@pytest.fixture
def sample_kost(kost_factory):
    """
    Menyediakan satu data kost contoh yang sudah tersimpan.

    Digunakan saat tes hanya memerlukan satu properti kost standar
    tanpa perlu konfigurasi tambahan.

    Returns:
        Kost: Objek kost contoh.
    """
    return kost_factory()

@pytest.fixture
def room_factory(db):
    """
    Membuat fungsi pembantu untuk menghasilkan data kamar.

    Fungsi ini membantu menyiapkan data unit kamar yang terkait dengan
    kost tertentu secara dinamis.

    Returns:
        function: Fungsi untuk membuat instance Room.
    """
    def create_room(kost, room_number="101", price=1000000, **kwargs):
        return Room.objects.create(
            kost=kost,
            room_number=room_number,
            price=price,
            **kwargs
        )
    return create_room

@pytest.fixture
def sample_room(sample_kost, room_factory):
    """
    Menyediakan satu data kamar contoh yang sudah tersimpan.

    Fixture ini secara otomatis menghubungkan kamar dengan kost contoh
    yang sudah ada di database.

    Returns:
        Room: Objek kamar contoh.
    """
    return room_factory(kost=sample_kost)