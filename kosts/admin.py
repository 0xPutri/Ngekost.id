from django.contrib import admin
from unfold.admin import ModelAdmin, TabularInline
from .models import Kost, KostImage, PaymentMethod, Room, RoomImage

class RoomInline(TabularInline):
    """
    Menampilkan kamar langsung di halaman admin kost.

    Konfigurasi ini memudahkan admin melihat relasi kost dan kamar dalam
    satu tampilan pengelolaan.
    """
    model = Room
    extra = 1
    tab = True


class KostImageInline(TabularInline):
    """
    Menampilkan galeri gambar langsung di halaman admin kost.

    Konfigurasi ini memudahkan admin atau owner internal melihat dan mengelola
    dokumentasi visual properti dalam satu halaman.
    """
    model = KostImage
    extra = 1
    tab = True


class RoomImageInline(TabularInline):
    """
    Menampilkan galeri gambar langsung di halaman admin kamar.

    Konfigurasi ini memudahkan pengelolaan visual kamar tanpa perlu membuka
    menu terpisah untuk setiap file gambar.
    """
    model = RoomImage
    extra = 1
    tab = True

@admin.register(Kost)
class KostAdmin(ModelAdmin):
    """
    Menata tampilan daftar kost pada panel admin Django.

    Konfigurasi ini membantu pencarian dan audit data kost secara cepat oleh
    administrator sistem.
    """
    list_display = ('name', 'owner', 'created_at')
    search_fields = ('name', 'address', 'owner__username')
    list_filter = ('created_at',)
    inlines = [RoomInline, KostImageInline]

@admin.register(Room)
class RoomAdmin(ModelAdmin):
    """
    Menata tampilan daftar kamar pada panel admin Django.

    Tampilan ini memudahkan admin memantau status kamar, harga, dan relasi
    kost secara ringkas.
    """
    list_display = ('room_number', 'kost', 'price', 'status')
    list_filter = ('status', 'kost')
    search_fields = ('room_number', 'kost__name')
    inlines = [RoomImageInline]


@admin.register(KostImage)
class KostImageAdmin(ModelAdmin):
    """
    Menata tampilan daftar gambar kost pada panel admin Django.

    Tampilan ini membantu pencarian gambar berdasarkan kost dan pengelolaan
    dokumentasi visual properti secara terpisah bila diperlukan.
    """
    list_display = ('kost', 'caption', 'created_at')
    list_filter = ('kost', 'created_at')
    search_fields = ('kost__name', 'caption')


@admin.register(RoomImage)
class RoomImageAdmin(ModelAdmin):
    """
    Menata tampilan daftar gambar kamar pada panel admin Django.

    Tampilan ini membantu pencarian gambar berdasarkan kamar dan pengelolaan
    dokumentasi visual unit secara terpisah bila diperlukan.
    """
    list_display = ('room', 'caption', 'created_at')
    list_filter = ('room', 'created_at')
    search_fields = ('room__room_number', 'room__kost__name', 'caption')

@admin.register(PaymentMethod)
class PaymentMethodAdmin(ModelAdmin):
    """
    Menata tampilan daftar metode pembayaran pada panel admin.
    """
    list_display = ('name', 'kost', 'created_at')
    list_filter = ('kost', 'created_at')
    search_fields = ('name', 'kost__name', 'kost__owner__username')