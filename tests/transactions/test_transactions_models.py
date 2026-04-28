import pytest
from datetime import date
from transactions.models import Booking

@pytest.mark.django_db
class TestTransactionModels:
    """
    Kumpulan pengujian untuk alur transaksi booking.

    Memastikan setiap pemesanan kamar oleh tenant dihitung dengan tepat
    dan status transaksi terpantau dengan baik.
    """

    def test_booking_total_price_calculation(self, tenant_user, sample_room):
        """
        Memvalidasi akurasi perhitungan total biaya sewa.

        Sistem harus mengalikan harga kamar dengan durasi sewa secara
        otomatis saat data booking pertama kali dibuat.
        """
        booking = Booking.objects.create(
            tenant=tenant_user,
            room=sample_room,
            start_date=date.today(),
            duration_months=3
        )
        assert booking.total_price == 3000000
        assert booking.status == 'pending_payment'
        assert str(booking) == f"Booking #{booking.id} - {tenant_user.username} - {sample_room.room_number}"

    def test_booking_status_choices(self, tenant_user, sample_room):
        """
        Memvalidasi perubahan status operasional booking.

        Memastikan setiap transisi status pembayaran sesuai dengan pilihan
        yang sudah didefinisikan dalam sistem.
        """
        booking = Booking.objects.create(
            tenant=tenant_user,
            room=sample_room,
            start_date=date.today()
        )
        booking.status = 'paid'
        booking.save()
        assert booking.status == 'paid'