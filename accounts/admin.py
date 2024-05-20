from django.contrib import admin
from django.contrib.admin.decorators import register
from django.contrib.auth.admin import UserAdmin as AbstractUserAdmin
from .models import *
from django.contrib.auth.models import Group


# ----------------------------- User ---------------------------------------
@register(User)
class UserAdmin(AbstractUserAdmin):
    
    list_display = ('username', 'first_name', 'last_name', 'email',
                    'is_active', 'is_staff', 'is_superuser', 'date_joined'
    )

    list_filter = ('is_active', 'is_superuser')
    search_fields = ('username', 'first_name', 'last_name', 'email')
    list_display_links = ('first_name', 'last_name', 'username')
    ordering = ('-is_superuser', '-is_staff', '-date_joined')

    fieldsets = (
        ('اطلاعات ورود', {
            'fields': ('username', 'password')
        }),

        ('اطلاعات شخصی', {
            'fields': ('first_name', 'last_name', 'email')
        }),

        ('دسترسی‌ها', {
            'fields': (
                'is_active',
                'is_staff',
                'is_superuser',
                'user_permissions',
            )
        }),

    )

    add_fieldsets = (
        ('اطلاعات ورود', {
            'fields': ('username', 'password1', 'password2')
        }),

        ('اطلاعات شخصی', {
            'fields': ('first_name', 'last_name', 'email')
        }),

        ('دسترسی‌ها', {
            'fields': (
                'is_active',
                'is_staff',
                'is_superuser',
                'user_permissions',
            )
        })
    )