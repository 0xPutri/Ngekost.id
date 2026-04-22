from django.contrib import admin
from unfold.admin import ModelAdmin, TabularInline
from .models import Kost, KostImage, PaymentMethod, Room, RoomImage
from core.admin_mixins import RoleBasedModelAdminMixin

class RoomInline(TabularInline):
    """
    Menampilkan kamar langsung di halaman admin kost.

    Konfigurasi ini memudahkan admin melihat relasi kost dan kamar dalam
    satu tampilan pengelolaan.
    """
    model = Room
    extra = 1
    tab = True

    def has_change_permission(self, request, obj=None):
        if hasattr(request.user, 'role') and request.user.role in ['admin', 'owner']:
            return True
        return False
    
    def has_add_permission(self, request, obj=None):
        return self.has_change_permission(request, obj)
        
    def has_delete_permission(self, request, obj=None):
        return self.has_change_permission(request, obj)

class KostImageInline(TabularInline):
    """
    Menampilkan galeri gambar langsung di halaman admin kost.

    Konfigurasi ini memudahkan admin atau owner internal melihat dan mengelola
    dokumentasi visual properti dalam satu halaman.
    """
    model = KostImage
    extra = 1
    tab = True
    
    def has_change_permission(self, request, obj=None):
        if hasattr(request.user, 'role') and request.user.role in ['admin', 'owner']:
            return True
        return False
    
    def has_add_permission(self, request, obj=None):
        return self.has_change_permission(request, obj)
        
    def has_delete_permission(self, request, obj=None):
        return self.has_change_permission(request, obj)

class RoomImageInline(TabularInline):
    """
    Menampilkan galeri gambar langsung di halaman admin kamar.

    Konfigurasi ini memudahkan pengelolaan visual kamar tanpa perlu membuka
    menu terpisah untuk setiap file gambar.
    """
    model = RoomImage
    extra = 1
    tab = True
    
    def has_change_permission(self, request, obj=None):
        if hasattr(request.user, 'role') and request.user.role in ['admin', 'owner']:
            return True
        return False
    
    def has_add_permission(self, request, obj=None):
        return self.has_change_permission(request, obj)
        
    def has_delete_permission(self, request, obj=None):
        return self.has_change_permission(request, obj)

@admin.register(Kost)
class KostAdmin(RoleBasedModelAdminMixin, ModelAdmin):
    """
    Menata tampilan daftar kost pada panel admin Django.

    Konfigurasi ini membantu pencarian dan audit data kost secara cepat oleh
    administrator sistem.
    """
    owner_field_path = 'owner'
    list_display = ('name', 'owner', 'created_at')
    search_fields = ('name', 'address', 'owner__username')
    list_filter = ('created_at',)
    inlines = [RoomInline, KostImageInline]

    def save_model(self, request, obj, form, change):
        if getattr(request.user, 'role', None) == 'owner' and not change:
            obj.owner = request.user
        super().save_model(request, obj, form, change)

    def get_fields(self, request, obj=None):
        fields = super().get_fields(request, obj)
        if getattr(request.user, 'role', None) == 'owner':
            if 'owner' in fields:
                fields.remove('owner')
        return fields

@admin.register(Room)
class RoomAdmin(RoleBasedModelAdminMixin, ModelAdmin):
    """
    Menata tampilan daftar kamar pada panel admin Django.

    Tampilan ini memudahkan admin memantau status kamar, harga, dan relasi
    kost secara ringkas.
    """
    owner_field_path = 'kost__owner'
    list_display = ('room_number', 'kost', 'price', 'status')
    list_filter = ('status', 'kost')
    search_fields = ('room_number', 'kost__name')
    inlines = [RoomImageInline]

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "kost" and getattr(request.user, 'role', None) == 'owner':
            kwargs["queryset"] = Kost.objects.filter(owner=request.user)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

@admin.register(KostImage)
class KostImageAdmin(RoleBasedModelAdminMixin, ModelAdmin):
    """
    Menata tampilan daftar gambar kost pada panel admin Django.

    Tampilan ini membantu pencarian gambar berdasarkan kost dan pengelolaan
    dokumentasi visual properti secara terpisah bila diperlukan.
    """
    owner_field_path = 'kost__owner'
    list_display = ('kost', 'caption', 'created_at')
    list_filter = ('kost', 'created_at')
    search_fields = ('kost__name', 'caption')

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "kost" and getattr(request.user, 'role', None) == 'owner':
            kwargs["queryset"] = Kost.objects.filter(owner=request.user)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

@admin.register(RoomImage)
class RoomImageAdmin(RoleBasedModelAdminMixin, ModelAdmin):
    """
    Menata tampilan daftar gambar kamar pada panel admin Django.

    Tampilan ini membantu pencarian gambar berdasarkan kamar dan pengelolaan
    dokumentasi visual unit secara terpisah bila diperlukan.
    """
    owner_field_path = 'room__kost__owner'
    list_display = ('room', 'caption', 'created_at')
    list_filter = ('room', 'created_at')
    search_fields = ('room__room_number', 'room__kost__name', 'caption')

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "room" and getattr(request.user, 'role', None) == 'owner':
            kwargs["queryset"] = Room.objects.filter(kost__owner=request.user)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

@admin.register(PaymentMethod)
class PaymentMethodAdmin(RoleBasedModelAdminMixin, ModelAdmin):
    """
    Menata tampilan daftar metode pembayaran pada panel admin.
    """
    owner_field_path = 'kost__owner'
    list_display = ('name', 'kost', 'created_at')
    list_filter = ('kost', 'created_at')
    search_fields = ('name', 'kost__name', 'kost__owner__username')

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "kost" and getattr(request.user, 'role', None) == 'owner':
            kwargs["queryset"] = Kost.objects.filter(owner=request.user)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)