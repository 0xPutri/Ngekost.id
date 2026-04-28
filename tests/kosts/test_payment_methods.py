import pytest
from django.db import IntegrityError
from kosts.models import PaymentMethod

@pytest.mark.django_db
class TestPaymentMethod:
    """
    Kumpulan pengujian untuk fitur metode pembayaran.

    Memastikan pemilik kost dapat mengelola opsi pembayaran QRIS atau
    transfer dengan validasi yang ketat.
    """

    def test_create_payment_method(self, sample_kost):
        """
        Memastikan metode pembayaran berhasil ditambahkan.

        Fungsi ini menguji apakah owner Hanna Fernanda bisa mendaftarkan
        opsi pembayaran baru untuk properti miliknya.
        """
        pm = PaymentMethod.objects.create(
            kost=sample_kost,
            name="QRIS",
            image="test_qris.png"
        )
        assert pm.name == "QRIS"
        assert pm.kost == sample_kost
        assert str(pm) == "Kost Sakura - QRIS"

    def test_payment_method_uniqueness(self, sample_kost):
        """
        Memvalidasi pencegahan duplikasi metode pembayaran.

        Sistem harus menolak jika owner mencoba mengunggah nama metode
        pembayaran yang sama untuk satu properti kost.
        """
        PaymentMethod.objects.create(kost=sample_kost, name="QRIS", image="q1.png")
        
        with pytest.raises(IntegrityError):
            PaymentMethod.objects.create(kost=sample_kost, name="QRIS", image="q2.png")

    def test_different_kost_same_payment_name(self, kost_factory):
        """
        Memastikan nama metode pembayaran yang sama boleh untuk kost berbeda.

        Validasi keunikan hanya berlaku dalam lingkup satu kost, sehingga
        kost lain tetap bisa menggunakan nama yang identik.
        """
        kost1 = kost_factory(name="Kost A")
        kost2 = kost_factory(name="Kost B")
        
        PaymentMethod.objects.create(kost=kost1, name="QRIS", image="q1.png")
        pm2 = PaymentMethod.objects.create(kost=kost2, name="QRIS", image="q2.png")
        
        assert pm2.id is not None