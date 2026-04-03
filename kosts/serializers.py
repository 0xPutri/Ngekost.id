from decimal import Decimal
from rest_framework import serializers
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema_field
from .models import Kost, Room

class RoomSerializer(serializers.ModelSerializer):
    def validate_kost(self, value):
        request = self.context.get('request')

        if request is None or request.method in ('GET', 'HEAD', 'OPTIONS'):
            return value

        if value.owner != request.user:
            raise serializers.ValidationError(
                "Anda hanya dapat mengelola kamar untuk kost milik Anda sendiri."
            )

        return value

    class Meta:
        model = Room
        fields = ['id', 'kost', 'room_number', 'price', 'status', 'description', 'created_at']
        read_only_fields = ['id', 'created_at']

class KostSerializer(serializers.ModelSerializer):
    min_price = serializers.SerializerMethodField()
    owner_name = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = Kost
        fields = ['id', 'owner', 'owner_name', 'name', 'address', 'description', 'facilities', 'latitude', 'longitude', 'min_price', 'created_at']
        read_only_fields = ['id', 'owner', 'created_at']

    @extend_schema_field(OpenApiTypes.DECIMAL)
    def get_min_price(self, obj) -> Decimal | None:
        rooms = obj.rooms.all()
        if rooms.exists():
            return min(room.price for room in rooms)
        return None
    
class KostDetailSerializer(KostSerializer):
    rooms = RoomSerializer(many=True, read_only=True)

    class Meta(KostSerializer.Meta):
        fields = KostSerializer.Meta.fields + ['rooms']