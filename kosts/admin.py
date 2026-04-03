from django.contrib import admin
from .models import Kost, Room

class RoomInline(admin.TabularInline):
    """
    Menampilkan kamar langsung di halaman admin kost.

    Konfigurasi ini memudahkan admin melihat relasi kost dan kamar dalam
    satu tampilan pengelolaan.
    """
    model = Room
    extra = 1

@admin.register(Kost)
class KostAdmin(admin.ModelAdmin):
    """
    Menata tampilan daftar kost pada panel admin Django.

    Konfigurasi ini membantu pencarian dan audit data kost secara cepat oleh
    administrator sistem.
    """
    list_display = ('name', 'owner', 'created_at')
    search_fields = ('name', 'address', 'owner__username')
    list_filter = ('created_at',)
    inlines = [RoomInline]

@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    """
    Menata tampilan daftar kamar pada panel admin Django.

    Tampilan ini memudahkan admin memantau status kamar, harga, dan relasi
    kost secara ringkas.
    """
    list_display = ('room_number', 'kost', 'price', 'status')
    list_filter = ('status', 'kost')
    search_fields = ('room_number', 'kost__name')