from django.contrib import admin
from django.contrib.admin.decorators import register
from django.contrib.auth.admin import UserAdmin as AbstractUserAdmin
from .models import *
from django.contrib.auth.models import Group


# ----------------------------- User ---------------------------------------
@register(User)
class UserAdmin(AbstractUserAdmin):
    
    list_display = ('username', 'first_name', 'last_name', 'get_user_subscription', 
                    'credits', 'email',
                    'is_active',  'access_all_coins', 'is_staff', 'is_superuser', 'date_joined'
    )

    list_filter = ('is_active', 'is_superuser', 'subscriptions')
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

@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    pass


@admin.register(RegisteredSubscription)
class RegisteredSubscriptionAdmin(admin.ModelAdmin):
    list_display = ('user', 'subscription', 'credits', 'status', \
                    'credits_period', 'is_active', 'credits_added', 'expire_at')
    list_filter = ('user', 'subscription', 'status', 'credits_added')
    list_editable = ('status', )