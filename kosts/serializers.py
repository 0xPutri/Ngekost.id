from decimal import Decimal
from rest_framework import serializers
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema_field
from .models import Kost, KostImage, PaymentMethod, Room, RoomImage


class RoomImageSerializer(serializers.ModelSerializer):
    """
    Menyajikan data gambar kamar untuk kebutuhan galeri pada API.

    Serializer ini bersifat baca agar gambar kamar langsung tampil pada
    response tanpa mengubah kontrak penulisan endpoint kamar yang ada.
    """

    class Meta:
        model = RoomImage
        fields = ['id', 'image', 'caption', 'created_at']
        read_only_fields = ['id', 'created_at']


class RoomImageWriteSerializer(serializers.ModelSerializer):
    """
    Memvalidasi pembuatan dan perubahan gambar kamar oleh owner.

    Serializer ini memastikan gambar hanya dapat dikaitkan ke kamar yang
    dimiliki oleh owner yang sedang login.
    """

    def validate_room(self, value):
        request = self.context.get('request')

        if request is None or request.method in ('GET', 'HEAD', 'OPTIONS'):
            return value

        if value.kost.owner != request.user:
            raise serializers.ValidationError(
                "Anda hanya dapat mengelola gambar untuk kamar pada kost milik Anda sendiri."
            )

        return value

    class Meta:
        model = RoomImage
        fields = ['id', 'room', 'image', 'caption', 'created_at']
        read_only_fields = ['id', 'created_at']

class RoomSerializer(serializers.ModelSerializer):
    """
    Menyajikan dan memvalidasi data kamar pada API kost.

    Serializer ini memastikan owner hanya dapat mengelola kamar yang berada
    pada kost miliknya sendiri.
    """
    images = RoomImageSerializer(many=True, read_only=True)

    def validate_kost(self, value):
        """
        Memastikan kost target memang dimiliki oleh owner yang sedang login.

        Args:
            value (Kost): Objek kost yang dipilih untuk kamar.

        Returns:
            Kost: Objek kost yang telah lolos validasi kepemilikan.

        Raises:
            ValidationError: Jika kost tidak dimiliki oleh pengguna aktif.
        """
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
        fields = ['id', 'kost', 'room_number', 'price', 'status', 'description', 'images', 'created_at']
        read_only_fields = ['id', 'created_at']


class KostImageSerializer(serializers.ModelSerializer):
    """
    Menyajikan data gambar kost untuk kebutuhan galeri pada API.

    Serializer ini hanya bersifat baca agar data visual kost dapat tampil
    pada response tanpa mengubah kontrak penulisan endpoint kost yang ada.
    """

    class Meta:
        model = KostImage
        fields = ['id', 'image', 'caption', 'created_at']
        read_only_fields = ['id', 'created_at']


class KostImageWriteSerializer(serializers.ModelSerializer):
    """
    Memvalidasi pembuatan dan perubahan gambar kost oleh owner.

    Serializer ini memastikan gambar hanya dapat dikaitkan ke kost milik
    owner yang sedang login.
    """

    def validate_kost(self, value):
        request = self.context.get('request')

        if request is None or request.method in ('GET', 'HEAD', 'OPTIONS'):
            return value

        if value.owner != request.user:
            raise serializers.ValidationError(
                "Anda hanya dapat mengelola gambar untuk kost milik Anda sendiri."
            )

        return value

    class Meta:
        model = KostImage
        fields = ['id', 'kost', 'image', 'caption', 'created_at']
        read_only_fields = ['id', 'created_at']

class KostSerializer(serializers.ModelSerializer):
    """
    Menyajikan data ringkas kost untuk daftar dan proses pengelolaan.

    Serializer ini menambahkan informasi harga minimum kamar agar tenant
    dapat membaca gambaran biaya sewa sejak halaman daftar.
    """
    min_price = serializers.SerializerMethodField()
    owner_name = serializers.ReadOnlyField(source='owner.username')
    images = KostImageSerializer(many=True, read_only=True)

    class Meta:
        model = Kost
        fields = ['id', 'owner', 'owner_name', 'name', 'address', 'description', 'facilities', 'latitude', 'longitude', 'min_price', 'images', 'created_at']
        read_only_fields = ['id', 'owner', 'created_at']

    @extend_schema_field(OpenApiTypes.DECIMAL)
    def get_min_price(self, obj) -> Decimal | None:
        """
        Mengambil harga kamar termurah dari sebuah kost.

        Args:
            obj (Kost): Objek kost yang sedang diserialisasi.

        Returns:
            Decimal | None: Harga minimum kamar, atau `None` jika belum ada kamar.
        """
        rooms = obj.rooms.all()
        if rooms.exists():
            return min(room.price for room in rooms)
        return None


class PaymentMethodSerializer(serializers.ModelSerializer):
    """
    Menyajikan data metode pembayaran secara ringkas.

    Serializer ini membantu API menampilkan informasi metode pembayaran
    dengan bentuk yang mudah dibaca oleh frontend.
    """
    class Meta:
        model = PaymentMethod
        fields = ['id', 'kost', 'name', 'image', 'created_at', 'updated_at']
        read_only_fields = ['id', 'kost', 'created_at', 'updated_at']


class KostDetailSerializer(KostSerializer):
    """
    Menyajikan detail kost lengkap beserta daftar kamarnya.

    Serializer ini dipakai saat tenant atau owner membuka satu kost secara
    spesifik dan membutuhkan informasi kamar sekaligus.
    """
    rooms = RoomSerializer(many=True, read_only=True)
    payment_methods = PaymentMethodSerializer(many=True, read_only=True)

    class Meta(KostSerializer.Meta):
        fields = KostSerializer.Meta.fields + ['rooms', 'payment_methods']