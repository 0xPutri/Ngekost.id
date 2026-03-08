from django.contrib import admin
from .models import Kost, Room

class RoomInline(admin.TabularInline):
    model = Room
    extra = 1

@admin.register(Kost)
class KostAdmin(admin.ModelAdmin):
    list_display = ('name', 'owner', 'created_at')
    search_fields = ('name', 'address', 'owner__username')
    list_filter = ('created_at',)
    inlines = [RoomInline]

@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ('room_number', 'kost', 'price', 'status')
    list_filter = ('status', 'kost')
    search_fields = ('room_number', 'kost__name')