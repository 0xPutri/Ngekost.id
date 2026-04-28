import pytest
from kosts.models import Kost, Room

@pytest.mark.django_db
class TestKostModels:
    """
    Kumpulan pengujian untuk model kost dan kamar.

    Memastikan data properti dan unit kamar tersimpan dengan aman serta
    terhubung satu sama lain dengan benar.
    """

    def test_kost_creation(self, sample_kost):
        """
        Memvalidasi penyimpanan data properti kost.

        Memastikan nama kost dan identitas pemilik Hanna Fernanda
        terekam secara akurat di database.
        """
        assert sample_kost.name == "Kost Sakura"
        assert sample_kost.owner.username == "owner_hanna"
        assert str(sample_kost) == "Kost Sakura - owner_hanna"

    def test_room_creation(self, sample_room):
        """
        Memvalidasi penyimpanan data unit kamar.

        Memastikan setiap nomor kamar terhubung secara konsisten ke
        properti kost induknya.
        """
        assert sample_room.room_number == "101"
        assert sample_room.kost.name == "Kost Sakura"
        assert str(sample_room) == "Kamar 101 - Kost Sakura"