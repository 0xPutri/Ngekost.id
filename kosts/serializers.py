from rest_framework import serializers
from .models import Kost, Room

class RoomSerializer(serializers.ModelSerializer):
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

    def get_min_price(self, obj):
        rooms = obj.rooms.all()
        if rooms.exists():
            return min(room.price for room in rooms)
        return None
    
class KostDetailSerializer(KostSerializer):
    rooms = RoomSerializer(many=True, read_only=True)

    class Meta(KostSerializer.Meta):
        fields = KostSerializer.Meta.fields + ['rooms']
