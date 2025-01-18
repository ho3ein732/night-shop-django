from django.contrib import admin
from .models import NightUser
from django.contrib.auth.admin import UserAdmin
from .forms import *


@admin.register(NightUser)
class NightDimondUserAdmin(UserAdmin):  # تغییر به UserAdmin
    ordering = ['email']
    model = NightUser
    add_form = NightUserCreationForm  # اصلاح اشتباه تایپی
    form = NightUserChangeForm
    list_display = ['id', 'email', 'first_name', 'last_name', 'is_active', 'is_staff', 'is_superuser']
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', )}),
    )

    add_fieldsets = (
        (None, {'fields': ('email', 'password1', 'password2')}),
        ('Personal info', {'fields': ('first_name', 'last_name')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login',)}),
    )