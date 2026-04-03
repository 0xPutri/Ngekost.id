from rest_framework import serializers
from .models import Booking, PaymentProof
from kosts.models import Room

class PaymentProofSerializer(serializers.ModelSerializer):
    """
    Menyajikan data unggahan bukti pembayaran pada API transaksi.

    Serializer ini dipakai saat tenant mengirim file pembayaran dan saat
    sistem menampilkan metadata unggahan tersebut.
    """
    class Meta:
        model = PaymentProof
        fields = ['id', 'image', 'uploaded_at']
        read_only_fields = ['id', 'uploaded_at']

class BookingSerializer(serializers.ModelSerializer):
    """
    Menyajikan data booking beserta informasi kamar dan kost terkait.

    Serializer ini membantu tenant, owner, dan admin membaca transaksi dengan
    konteks properti yang lebih jelas.
    """
    payment_proof = PaymentProofSerializer(read_only=True)
    room_details = serializers.CharField(source='room.room_number', read_only=True)
    kost_name = serializers.CharField(source='room.kost.name', read_only=True)

    class Meta:
        model = Booking
        fields = ['id', 'room', 'room_details', 'kost_name', 'start_date', 'duration_months', 'total_price', 'status', 'payment_proof', 'created_at']
        read_only_fields = ['id', 'total_price', 'status', 'created_at']

    def validate_room(self, value):
        """
        Memastikan kamar yang dipilih masih tersedia untuk dibooking.

        Args:
            value (Room): Kamar yang dipilih tenant.

        Returns:
            Room: Kamar yang valid untuk proses booking.

        Raises:
            ValidationError: Jika status kamar tidak tersedia.
        """
        if value.status != 'available':
            raise serializers.ValidationError("Kamar ini tidak tersedia untuk dipesan.")
        return value