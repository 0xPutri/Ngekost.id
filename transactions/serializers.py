from rest_framework import serializers
from .models import Booking, PaymentProof
from kosts.models import Room

class PaymentProofSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentProof
        fields = ['id', 'image', 'uploaded_at']
        read_only_fields = ['id', 'uploaded_at']

class BookingSerializer(serializers.ModelSerializer):
    payment_proof = PaymentProofSerializer(read_only=True)
    room_details = serializers.CharField(source='room.room_number', read_only=True)
    kost_name = serializers.CharField(source='room.kost.name', read_only=True)

    class Meta:
        model = Booking
        fields = ['id', 'room', 'room_details', 'kost_name', 'start_date', 'duration_months', 'total_price', 'status', 'payment_proof', 'created_at']
        read_only_fields = ['id', 'total_price', 'status', 'created_at']

    def validate_room(self, value):
        if value.status != 'available':
            raise serializers.ValidationError("Kamar ini tidak tersedia untuk dipesan.")
        return value