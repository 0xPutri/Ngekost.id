from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from unfold.admin import ModelAdmin
from unfold.forms import AdminPasswordChangeForm, UserChangeForm, UserCreationForm
from .models import CustomUser

@admin.register(CustomUser)
class CustomUserAdmin(ModelAdmin, BaseUserAdmin):
    """
    Menata tampilan data pengguna pada panel admin Django.

    Konfigurasi ini membantu administrator melihat identitas pengguna dan
    informasi peran tambahan secara lebih rapi.
    """
    form = UserChangeForm
    add_form = UserCreationForm
    change_password_form = AdminPasswordChangeForm

    model = CustomUser
    list_display = ['username', 'email', 'first_name', 'last_name', 'role', 'is_staff']
    fieldsets = BaseUserAdmin.fieldsets + (
        ('Informasi Tambahan', {'fields': ('role', 'phone_number')}),
    )
    add_fieldsets = BaseUserAdmin.add_fieldsets + (
        ('Informasi Tambahan', {'fields': ('role', 'phone_number')}),
    )